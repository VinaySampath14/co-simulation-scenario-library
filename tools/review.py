"""Collect selected evidence and generate a human-review packet."""

import gzip
import hashlib
from html.parser import HTMLParser
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
from urllib.parse import quote, urlsplit
from urllib.request import Request, urlopen
import zipfile

from jsonschema import Draft202012Validator, ValidationError

if __package__:
    from .validate import ROOT, pdf_part, request_review, scenario_packet, settings
else:
    from validate import ROOT, pdf_part, request_review, scenario_packet, settings


TEXT_LIMIT = 750_000
GIT_SHA = re.compile(r"[a-fA-F0-9]{40}(?:[a-fA-F0-9]{24})?")
FINDING_TYPES = (
    "supported", "contradicted", "needs_evidence", "missing_metadata",
    "possible_hallucination", "model_identity_concern", "human_question",
)


class DocumentText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.fragments = []
        self.hidden = 0

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style"}:
            self.hidden += 1
        elif tag in {"p", "li", "h1", "h2", "h3", "br", "tr"}:
            self.fragments.append("\n")

    def handle_endtag(self, tag):
        if tag in {"script", "style"}:
            self.hidden = max(0, self.hidden - 1)

    def handle_data(self, data):
        if not self.hidden:
            self.fragments.append(data)


def text_part(data, metadata, html=False, display_data=None):
    selected = display_data if display_data is not None else data
    if len(selected) > TEXT_LIMIT:
        raise ValueError("Text artifact exceeds 750 KB. Supply a smaller artifact or a pinned line range.")
    body = selected.decode("utf-8-sig")
    if html:
        parser = DocumentText()
        parser.feed(body)
        body = "\n".join(line.strip() for line in "".join(parser.fragments).splitlines() if line.strip())
    if not body.strip():
        raise ValueError("The selected artifact contains no readable text.")
    if "commit" in metadata or "archive_sha256" in metadata:
        first = metadata.get("line_start", 1)
        body = "\n".join(f"{n}: {line}" for n, line in enumerate(body.splitlines(), first))
    return {"type": "input_text", "text": json.dumps(metadata, ensure_ascii=False) + "\n" + body}


def git_blob(checkout, source, entry):
    revision = source.get("version_or_commit") or ""
    path = entry["path"]
    relative = PurePosixPath(path)
    if not GIT_SHA.fullmatch(revision) or relative.is_absolute() or ".." in relative.parts or ":" in path or "\\" in path:
        raise ValueError("Pinned Git artifacts require a full commit hash and a repository-relative path.")
    git = shutil.which("git")
    if not git:
        git = str(Path("C:/Program Files/Git/cmd/git.exe"))
    command = [git, "-C", str(checkout.resolve()), "-c", f"safe.directory={checkout.resolve().as_posix()}"]

    def read(*arguments):
        result = subprocess.run(
            [*command, *arguments], capture_output=True, timeout=15, check=False,
            env=os.environ | {"GIT_NO_LAZY_FETCH": "1"},
        )
        if result.returncode:
            raise ValueError("Git could not read the requested origin, commit or blob.")
        return result.stdout

    origin = read("remote", "get-url", "origin").decode().strip()
    if origin.removesuffix(".git").rstrip("/") != source["url"].removesuffix(".git").rstrip("/"):
        raise ValueError("The checkout origin differs from the registered source URL.")
    if read("cat-file", "-t", revision).strip() != b"commit":
        raise ValueError("The registered revision is not a Git commit.")
    blob = f"{revision}:{path}"
    if read("cat-file", "-t", blob).strip() != b"blob":
        raise ValueError("The requested Git path does not identify a file.")
    ranged = "line_start" in entry or "line_end" in entry
    if int(read("cat-file", "-s", blob)) > (20_000_000 if ranged else TEXT_LIMIT):
        raise ValueError("Pinned Git artifact exceeds the size limit.")
    data = read("cat-file", "blob", blob)
    metadata = {"commit": revision, "path": path, "url": source["url"]}
    if ranged:
        first = entry.get("line_start", 1)
        last = entry.get("line_end")
        if type(first) is not int or type(last) is not int or not 1 <= first <= last <= 100_000:
            raise ValueError("Invalid pinned artifact line range.")
        metadata.update(line_start=first, line_end=last)
        stream = gzip.GzipFile(fileobj=io.BytesIO(data)) if path.endswith(".gz") else io.BytesIO(data)
        excerpt = bytearray()
        with stream:
            for number in range(1, last + 1):
                line = stream.readline(TEXT_LIMIT + 1)
                if not line or len(line) > TEXT_LIMIT:
                    raise ValueError("Pinned line range exceeds the artifact or a line is too large.")
                if number >= first:
                    excerpt.extend(line)
                    if len(excerpt) > TEXT_LIMIT:
                        raise ValueError("Pinned line range exceeds 750 KB.")
        if path.endswith(".gz"):
            metadata["line_basis"] = "decompressed"
        return metadata, data, bytes(excerpt)
    return metadata, data, None


def collect_sources(args, scenario, records):
    entries = []
    primary = scenario["scientific_publication_id"]
    primary_source = records[primary]["source_id"] if primary else scenario["source_ids"][0]
    for path in args.source:
        entries.append({"kind": "local", "source_id": primary_source, "path": str(path)})
    if args.manifest:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        if manifest["scenario_id"] != scenario["id"]:
            raise ValueError("The source manifest is for a different scenario.")
        entries.extend(manifest["artifacts"])

    parts = []
    artifacts = []
    archive = getattr(args, "archive", None)
    archive_hash = None
    for number, entry in enumerate(entries, 1):
        source_id = entry["source_id"]
        if source_id not in scenario["source_ids"]:
            raise ValueError(f"Source {source_id} is outside the selected scenario.")
        source = records[source_id]
        artifact = {"artifact_id": f"A{number}", "source_id": source_id, "url": source["url"], "kind": entry["kind"]}
        try:
            if entry["kind"] == "git":
                if args.git_checkout is None:
                    raise ValueError("Supply --git-checkout for pinned Git artifacts.")
                metadata, data, excerpt = git_blob(args.git_checkout, source, entry)
                artifact.update(metadata)
                part = text_part(data, artifact, display_data=excerpt)
            elif entry["kind"] == "archive":
                if archive is None:
                    raise ValueError("Supply --archive for checksum-pinned ZIP entries.")
                if archive_hash is None:
                    with archive.open("rb") as stream:
                        archive_hash = hashlib.file_digest(stream, "sha256").hexdigest()
                if source["url"] != f"urn:sha256:{archive_hash}":
                    raise ValueError("ZIP checksum differs from the registered source.")
                artifact.update(path=entry["path"], archive_sha256=archive_hash)
                with zipfile.ZipFile(archive) as bundle:
                    member = bundle.getinfo(entry["path"])
                    if member.file_size > TEXT_LIMIT:
                        raise ValueError("ZIP member exceeds 750 KB.")
                    data = bundle.read(member)
                part = text_part(data, artifact)
            elif entry["kind"] == "public_document":
                if urlsplit(source["url"]).scheme != "https":
                    raise ValueError("Public documentation must use HTTPS.")
                with urlopen(Request(source["url"], headers={"User-Agent": "ScenarioCatalogueReview/1.0"}), timeout=20) as response:
                    data = response.read(TEXT_LIMIT + 1)
                    artifact["retrieved_url"] = response.geturl()
                    part = text_part(data, artifact, html=response.headers.get_content_type() == "text/html")
            elif entry["kind"] == "local":
                path = Path(entry["path"])
                if args.manifest and not path.is_absolute() and path not in args.source:
                    path = args.manifest.parent / path
                artifact["path"] = path.name
                if path.suffix.lower() == ".pdf":
                    part, artifact["sha256"] = pdf_part(path)
                    part["filename"] = f"{artifact['artifact_id']}-{path.name}"
                    data = None
                elif path.suffix.lower() in {".md", ".txt", ".rst", ".py", ".json", ".csv", ".yaml", ".yml", ".toml", ".lock", ".xml", ".html"}:
                    if path.stat().st_size > TEXT_LIMIT:
                        raise ValueError("Local text artifact exceeds 750 KB.")
                    data = path.read_bytes()
                    part = text_part(data, artifact, html=path.suffix.lower() == ".html")
                else:
                    raise ValueError("Unsupported local artifact format.")
            else:
                raise ValueError("Unknown artifact kind.")
            if data is not None:
                artifact["sha256"] = hashlib.sha256(data).hexdigest()
            artifact["status"] = "supplied"
            parts.append(part)
        except (OSError, ValueError, KeyError, zipfile.BadZipFile, subprocess.TimeoutExpired) as error:
            artifact.update(status="unavailable", limitation=str(error))
        artifacts.append(artifact)
    return parts, artifacts


def review_findings(parts, artifacts, packet, config):
    fields = {
        "category": {"type": "string", "enum": list(FINDING_TYPES)},
        **{key: {"type": "string"} for key in ("catalogue_field", "claim", "artifact_id", "locator", "explanation", "recommended_correction")},
    }
    schema = {
        "type": "object",
        "properties": {
            "source_assessment": {"type": "string", "enum": ["consistent", "mismatch", "unclear"]},
            "limitations": {"type": "array", "items": {"type": "string"}},
            "findings": {
                "type": "array",
                "items": {"type": "object", "properties": fields, "required": list(fields), "additionalProperties": False},
            },
        },
        "required": ["source_assessment", "limitations", "findings"],
        "additionalProperties": False,
    }
    supplied = {artifact["artifact_id"]: artifact for artifact in artifacts if artifact["status"] == "supplied"}
    manifest = json.dumps(supplied, ensure_ascii=False)
    print("Reviewer API 1/2: extracting claims from the sources.", file=sys.stderr, flush=True)
    extraction = request_review(
        config, parts,
        "Read the evidence independently. Extract scenario scope, model identities, roles, "
        "directional exchanges, settings, outcomes and gaps. Look beyond standard metadata "
        "for details that affect interpretation, reuse or reproduction, including assumptions, "
        "initialization, artifact availability and terms of reuse. Give artifact IDs and precise "
        "locators. Distinguish code, explicit statements and inference. Artifacts: " + manifest,
    )
    print("Reviewer API 2/2: comparing the catalogue with the sources.", file=sys.stderr, flush=True)
    result = request_review(
        config, parts,
        "Compare the independently extracted facts and catalogue against the source artifacts. "
        "Check that the primary evidence matches the scenario. If it does not, report mismatch "
        "and withhold findings. Judge actual claims by record ID and field. Check whether its "
        "citation supports each claim as worded. Include missing or reversed data paths, "
        "uncertain model identity, unsupported conclusions and important omissions when present, "
        "including relevant details with no dedicated catalogue field. Check license claims "
        "separately for each paper, model implementation, FMU and dataset. "
        "Give an artifact ID and exact locator for evidential judgments. For code cite the "
        "supplied line numbers. Use an empty artifact_id or locator for an unresolved question "
        "without evidence. Explicit unknowns are only omissions when the evidence supplies the "
        "value. Recommend catalogue corrections only. Preserve quirks already catalogued "
        "faithfully. Treat unavailable sources as evidence gaps. Keep the report concise.\n\n"
        f"Artifacts: {manifest}\nIndependent extraction: {extraction}\n"
        f"Catalogue: {json.dumps(packet, ensure_ascii=False)}",
        {"type": "json_schema", "name": "scenario_review", "strict": True, "schema": schema},
    )
    result = json.loads(result)
    try:
        Draft202012Validator(schema).validate(result)
    except ValidationError as error:
        raise ValueError(f"Reviewer output failed its schema at {error.json_path}.") from error
    if result["source_assessment"] == "mismatch":
        result["findings"] = []
    return result


def check_finding_locators(result, artifacts):
    supplied_ids = {artifact["artifact_id"] for artifact in artifacts if artifact["status"] == "supplied"}
    for finding in result["findings"]:
        if finding["category"] in {"supported", "contradicted", "missing_metadata", "possible_hallucination"} and (
            finding["artifact_id"] not in supplied_ids or not finding["locator"].strip()
        ):
            finding["category"] = "needs_evidence"
            finding["explanation"] = "The reviewer did not supply a usable artifact locator. " + finding["explanation"]


def report_links(args, packet, scenario_id):
    paths = sorted(key for key in packet if key.endswith(".yaml"))
    paths.append(f"scenarios/{scenario_id}/description.md")
    paths.extend(
        f"{'models' if key.startswith('MOD-') else 'publications'}/{key}.yaml"
        for key in sorted(packet["referenced_records"])
        if key.startswith(("MOD-", "PUB-"))
    )
    paths.extend(("software/software.yaml", "evidence/evidence.yaml"))
    if not args.github_repo:
        output = (args.output_dir / scenario_id).resolve()
        return {path: Path(os.path.relpath(ROOT / path, output)).as_posix() for path in paths}
    if not re.fullmatch(r"[\w.-]+/[\w.-]+", args.github_repo):
        raise ValueError("--github-repo must be owner/repository.")
    base = f"https://github.com/{args.github_repo}/blob/{quote(args.github_revision, safe='')}/"
    return {path: base + path for path in paths}


def render_report(report):
    lines = [
        f"# {report['scenario_id']} — {report['title']}", "",
        "## Deterministic validation", "",
        f"Catalogue checks: **{report['structural_validation']['status']}** "
        f"({report['structural_validation']['yaml_files']} YAML files, "
        f"{report['structural_validation']['unique_ids']} IDs).",
        f"Review status: `{report['review_status']}`. "
        f"Declared human workflow status: `{report['declared_review_status']}`. "
        f"Runtime status: `{report['runtime_status']}`.", "",
        f"Catalogue packet SHA-256: `{report['catalogue_sha256']}`.", "",
        "## Review index", "",
    ]
    lines.extend(f"- [{path}]({link})" for path, link in report["links"].items())
    lines.extend(["", "## Original sources and review inputs", ""])
    if report["publication"]:
        publication = report["publication"]
        lines.append(f"- Primary publication: [{publication['title']}]({publication['url']})")
    for source in report["sources"]:
        revision = f" at `{source['version_or_commit']}`" if source.get("version_or_commit") else ""
        lines.append(f"- {source['id']} [{source['title']}]({source['url']}){revision}")
    for artifact in report["artifacts"]:
        location = artifact.get("path") or artifact["url"]
        fingerprint = artifact.get("sha256") or artifact.get("limitation", "")
        line_range = f" lines {artifact['line_start']}–{artifact['line_end']}" if "line_start" in artifact else ""
        lines.append(f"- {artifact['artifact_id']} ({artifact['source_id']}) {location}{line_range} — {artifact['status']}. {fingerprint}")
    ai = report["ai_review"]
    lines.extend(["", "## AI-assisted evidence review", "", f"Status: **{ai['status']}**."])
    if ai.get("model"):
        lines.append(f"Reviewer: `{ai['model']}`. Source assessment: `{ai.get('source_assessment', 'unavailable')}`.")
    lines.extend(["", "The findings require human judgment. The review does not approve the scenario.", ""])
    lines.extend(f"- {limitation}" for limitation in ai["limitations"])
    for category in (*FINDING_TYPES[1:], "supported"):
        findings = [finding for finding in ai["findings"] if finding["category"] == category]
        if findings:
            lines.extend(["", f"### {category.replace('_', ' ').capitalize()} ({len(findings)})", ""])
        for finding in findings:
            field = finding["catalogue_field"] or "No existing field"
            evidence = f"{finding['artifact_id']} {finding['locator']}".strip() or "Unresolved"
            action = finding["recommended_correction"] or "Review the cited evidence."
            lines.extend([
                f"- **{finding['claim']}**",
                f"  - Catalogue: {field}",
                f"  - Evidence: {evidence}",
                f"  - Assessment: {finding['explanation']}",
                f"  - Suggested action: {action}",
            ])
    return "\n".join(lines) + "\n"


def run_reviews(args, documents, records):
    identifiers = [args.scenario] if args.scenario else sorted(key for key in records if key.startswith("SCN-"))
    for scenario_id in identifiers:
        scenario = records[scenario_id]
        packet = scenario_packet(scenario_id, documents, records)
        publication = records.get(scenario["scientific_publication_id"])
        if publication:
            publication = {"title": publication["title"], "url": records[publication["source_id"]]["url"]}
        ai = {"status": "not_run", "limitations": ["Independent source review is pending."], "findings": []}
        artifacts = []
        failure = None
        output = args.output_dir / scenario_id
        fingerprint = hashlib.sha256(json.dumps(packet, sort_keys=True).encode()).hexdigest()
        previous = output / "review.json"
        if not (args.source or args.manifest) and previous.is_file():
            saved = json.loads(previous.read_text(encoding="utf-8"))
            if saved.get("catalogue_sha256") == fingerprint and saved["ai_review"]["status"] == "completed":
                ai = saved["ai_review"]
                artifacts = saved["artifacts"]
            elif saved["ai_review"]["status"] == "completed":
                ai["limitations"] = ["The catalogue changed since the previous evidence review. Rerun source review."]
        if args.source or args.manifest:
            config = settings()
            config.setdefault("VALIDATION_MODEL", "gpt-5-mini")
            try:
                parts, artifacts = collect_sources(args, scenario, records)
                if not parts:
                    raise ValueError("There are no readable source artifacts for review.")
                if not config.get("OPENAI_API_KEY") or not config.get("VALIDATION_MODEL"):
                    raise ValueError("Set OPENAI_API_KEY and VALIDATION_MODEL in .env or the environment.")
                ai = {"status": "completed", "model": config["VALIDATION_MODEL"], **review_findings(parts, artifacts, packet, config)}
            except (OSError, ValueError, KeyError, TypeError) as error:
                failure = str(error)
                ai = {"status": "failed", "limitations": [failure], "findings": []}
        check_finding_locators(ai, artifacts)
        evidence_checked = ai["status"] == "completed" and ai["source_assessment"] == "consistent"
        report = {
            "scenario_id": scenario_id, "title": scenario["title"],
            "publication": publication,
            "sources": [records[key] for key in scenario["source_ids"]],
            "artifacts": artifacts,
            "links": report_links(args, packet, scenario_id),
            "catalogue_sha256": fingerprint,
            "structural_validation": {"status": "passed", "yaml_files": len(documents), "unique_ids": len(records)},
            "review_status": "evidence_checked" if evidence_checked else "structurally_validated",
            "declared_review_status": scenario.get("review_status", "draft"),
            "runtime_status": scenario.get("runtime_verification_status", "not_run"),
            "ai_review": ai,
        }
        output.mkdir(parents=True, exist_ok=True)
        markdown = render_report(report)
        (output / "review.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (output / "review.md").write_text(markdown, encoding="utf-8")
        print(f"Wrote {output / 'review.md'} and review.json", file=sys.stderr)
        if args.source or args.manifest:
            print(markdown)
        if failure:
            raise ValueError(failure)
