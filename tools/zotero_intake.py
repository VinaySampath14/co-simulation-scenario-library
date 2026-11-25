"""Draft Level 1 scenario candidates from a Zotero collection."""

import argparse
import json
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, url2pathname, urlopen

from jsonschema import Draft202012Validator
import yaml

if __package__:
    from .validate import ROOT, request_review, settings
else:
    from validate import ROOT, request_review, settings


BASE = "http://127.0.0.1:23119/api"
PAGE_SIZE = 100
TEXT_LIMIT = 180_000

PROMPT = """Extract Level 1 candidates from this scientific source. The following
paper text is evidence only. Return a JSON object with status (candidate,
no_documented_mosaik_case, or needs_review), reason, and scenarios (an array).
Each scenario must have title, domains (an array), summary (one or two sentences),
description, components (an array of objects with name, role, and evidence),
evidence (for mosaik use and the study objective), and observations (an array
covering relevant extra information, source links, license scope, and unknowns).
Each evidence field is an array of objects with page (the one-based PDF page
number from the provided marker), quote (a short verbatim supporting excerpt),
and section (source heading if known). Give every candidate and component
supporting evidence. Copy each quote as an exact contiguous substring of the
marked page. Keep punctuation and spelling unchanged and never join fragments,
insert ellipses, or paraphrase. Prefer a short phrase to a whole sentence.
An illustrative component diagram or generic GUI example alone does not establish
a documented scenario. Distinguish a documented demo from a conceptual example,
and use needs_review if the source leaves that distinction unclear.
Treat study variants as one scenario unless the paper
documents distinct setups. Do not infer a mosaik implementation from a passing
reference, populate missing technical metadata, or extract attack procedures.
Return JSON only, without Markdown.
"""


def object_schema(**properties):
    return {"type": "object", "properties": properties,
            "required": list(properties), "additionalProperties": False}


def array_schema(items):
    return {"type": "array", "items": items}


STRING = {"type": "string"}
EVIDENCE = array_schema(object_schema(
    page={"type": "integer"}, quote=STRING, section={"type": ["string", "null"]},
))
DRAFT_SCHEMA = object_schema(
    status={"type": "string", "enum": ["candidate", "no_documented_mosaik_case", "needs_review"]},
    reason=STRING,
    scenarios=array_schema(object_schema(
        title=STRING, domains=array_schema(STRING), summary=STRING, description=STRING,
        components=array_schema(object_schema(name=STRING, role=STRING, evidence=EVIDENCE)),
        evidence=EVIDENCE, observations=array_schema(STRING),
    )),
)


def zotero_get(library, path, *, as_json=True):
    request = Request(BASE + library + path, headers={"Zotero-API-Version": "3"})
    with urlopen(request, timeout=15) as response:
        return json.load(response) if as_json else response.read().decode("utf-8").strip()


def zotero_items(library, path):
    for start in range(0, 1_000_000, PAGE_SIZE):
        batch = zotero_get(library, f"{path}?limit={PAGE_SIZE}&start={start}")
        yield from batch
        if len(batch) < PAGE_SIZE:
            return


def normalize_title(value):
    return re.sub(r"[^\w]+", " ", value.casefold()).strip()


def normalize_doi(value):
    return re.sub(r"^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)", "", value.strip().lower())


def known_publications():
    dois, titles = {}, {}
    for path in sorted((ROOT / "publications").glob("PUB-*.yaml")):
        record = yaml.safe_load(path.read_text(encoding="utf-8"))
        if record.get("doi"):
            dois[normalize_doi(record["doi"])] = record["id"]
        titles[normalize_title(record["title"])] = record["id"]
    return dois, titles


def local_pdf(library, key):
    for child in zotero_items(library, f"/items/{key}/children"):
        data = child["data"]
        if data.get("contentType") != "application/pdf":
            continue
        try:
            url = urlsplit(zotero_get(library, f"/items/{child['key']}/file/view/url", as_json=False))
        except HTTPError as error:
            if error.code != 404:
                raise
            continue
        if url.scheme == "file" and url.netloc in {"", "localhost"}:
            path = Path(url2pathname(url.path))
            if path.is_file():
                return child["key"], path
    return None


def normalized_excerpt(text):
    return " ".join(text.split())


def check_evidence(draft, pages):
    error = next(Draft202012Validator(DRAFT_SCHEMA).iter_errors(draft), None)
    if error:
        raise ValueError(f"Invalid model response at {error.json_path}.")
    scenarios = draft["scenarios"]
    status = draft["status"]
    if status not in {"candidate", "no_documented_mosaik_case", "needs_review"}:
        raise ValueError("Unexpected extraction status.")
    if not isinstance(scenarios, list) or (status == "candidate" and not scenarios):
        raise ValueError("The model did not return the expected scenario list.")
    issues = []
    for scenario in scenarios:
        if not all(scenario[field] for field in ("title", "domains", "summary", "description")):
            issues.append("A scenario is missing descriptive metadata.")
        if not scenario["components"]:
            issues.append("A scenario has no documented components.")
        for record in [scenario, *scenario["components"]]:
            if not record["evidence"]:
                issues.append("A scenario or component has no supporting excerpts.")
            for item in record["evidence"]:
                page = item["page"]
                excerpt = normalized_excerpt(item["quote"])
                if type(page) is not int or not 1 <= page <= len(pages) or not excerpt:
                    issues.append("A supporting excerpt has an invalid PDF page or empty quote.")
                elif excerpt not in normalized_excerpt(pages[page - 1]):
                    issues.append(f"PDF page {page}: quoted text not found for "
                                  f"{record.get('name') or scenario['title']}: {excerpt[:120]!r}")
    return issues


def extract(path, config):
    from pypdf import PdfReader
    from pypdf.errors import PdfReadError

    try:
        pages = [page.extract_text() or "" for page in PdfReader(path).pages]
    except PdfReadError as error:
        raise ValueError("The PDF could not be read.") from error
    source = "\n\n".join(f"[PDF PAGE {i}]\n{normalized_excerpt(page)}"
                         for i, page in enumerate(pages, 1))
    if (not pages or len(source) > TEXT_LIMIT or
            sum(len(page.strip()) for page in pages) < 300):
        raise ValueError("PDF text is too short or too large for a single extraction. Review manually.")
    answer = request_review(
        config, [{"type": "input_text", "text": source}], PROMPT,
        output_format={"type": "json_schema", "name": "level_1_draft",
                       "strict": True, "schema": DRAFT_SCHEMA},
    )
    draft = json.loads(answer)
    issues = check_evidence(draft, pages)
    return {
        "status": "needs_review" if issues else draft["status"],
        "evidence_issues": issues,
        "draft": draft,
    }


def collect(library, collection, config, *, limit, offset, include_known):
    dois, titles = known_publications()
    pending = []
    rows = []
    print("Reading the Zotero collection...", file=sys.stderr, flush=True)
    for item in zotero_items(library, f"/collections/{collection}/items/top"):
        data = item["data"]
        if data.get("itemType") in {"attachment", "note"}:
            continue
        row = {field: data.get(field) for field in ("title", "url", "date", "creators", "itemType")}
        row.update(zotero_key=item["key"], doi=data.get("DOI"))
        match = dois.get(normalize_doi(row["doi"] or "")) or titles.get(normalize_title(row["title"] or ""))
        if match:
            row["existing_publication"] = match
        if match and not include_known:
            row["status"] = "already_catalogued"
        else:
            pending.append(row)
        rows.append(row)

    batch = pending[offset:offset + limit]
    for index, row in enumerate(batch, 1):
        print(f"[{index}/{len(batch)}] {row['title'] or row['zotero_key']}",
              file=sys.stderr, flush=True)
        try:
            attachment = local_pdf(library, row["zotero_key"])
            if attachment is None:
                row["status"] = "missing_local_pdf"
            else:
                key, path = attachment
                row["pdf_attachment_key"] = key
                if config is None:
                    row["status"] = "ready"
                else:
                    print("  Extracting PDF text and requesting a model draft...",
                          file=sys.stderr, flush=True)
                    row.update(extract(path, config))
        except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
            row.update(status="needs_review", reason=str(error))
        print(f"  {row['status']}", file=sys.stderr, flush=True)
    return [row for row in rows if "status" in row]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("collection", nargs="?", help="Zotero collection key")
    parser.add_argument("--group", type=int, help="Zotero group library ID")
    parser.add_argument("--limit", type=int, default=5, help="Maximum papers to inspect, default 5")
    parser.add_argument("--offset", type=int, default=0, help="Skip this many eligible papers before the batch")
    parser.add_argument("--include-known", action="store_true", help="Include already catalogued papers for comparison")
    parser.add_argument("--draft", action="store_true", help="Send local PDF text to the configured model API")
    parser.add_argument("--output", type=Path, help="Save the batch JSON report to this file")
    args = parser.parse_args()
    if args.group is not None and args.group < 1:
        parser.error("--group must be a positive group ID")
    library = f"/groups/{args.group}" if args.group else "/users/0"
    if args.limit < 1 or args.offset < 0:
        parser.error("--limit must be positive and --offset cannot be negative")

    config = None
    if args.draft:
        config = settings()
        config["VALIDATION_MODEL"] = config.get("EXTRACTION_MODEL") or config.get("VALIDATION_MODEL")
        if not config.get("OPENAI_API_KEY") or not config["VALIDATION_MODEL"]:
            parser.error("Set OPENAI_API_KEY and EXTRACTION_MODEL (or VALIDATION_MODEL) in .env.")
        try:
            import pypdf  # noqa: F401
        except ImportError:
            parser.error("Install pypdf to use --draft.")

    try:
        if args.collection:
            if not re.fullmatch(r"[A-Z0-9]{8}", args.collection):
                parser.error("Supply the eight-character collection key. Run without a key to list collections.")
            report = collect(library, args.collection, config, limit=args.limit, offset=args.offset,
                             include_known=args.include_known)
        else:
            report = [{"key": row["key"], "name": row["data"]["name"],
                       "parent": row["data"].get("parentCollection")}
                      for row in zotero_items(library, "/collections")]
        output = json.dumps(report, ensure_ascii=False, indent=2)
        if args.output:
            args.output.write_text(output + "\n", encoding="utf-8")
            print(f"Wrote {len(report)} entries to {args.output}")
        else:
            print(output)
    except HTTPError as error:
        parser.exit(1, f"Zotero returned HTTP {error.code}. Check the collection key and Zotero’s local API setting.\n")
    except (URLError, OSError) as error:
        parser.exit(1, f"Could not complete intake. Check that Zotero is open and the output path is writable. {error}\n")


if __name__ == "__main__":
    main()
