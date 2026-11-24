# Scenario review workflow

Use this workflow from the repository root in the VS Code PowerShell terminal. The catalogue records what a source supports. The review report tracks what was checked and what needs a decision.

## 1. Collect a draft

Give Codex the paper or source and ask it to follow the [collection protocol](SCENARIO_COLLECTION_PROTOCOL.md). Keep a separate scenario record, participations, interactions, and description. Reuse a model ID only when the definition matches. Record evidence IDs and original locators for important claims. Use `null` for a known gap and explain why the value cannot be established.

New evidence can distinguish `explicitly_reported`, `verified_from_code`, `inferred`, `not_reported`, `not_yet_investigated`, or `conflicting`. For a code claim, register the repository URL and commit and give the file path and line range in the assertion. For a paper, register the DOI or stable URL and cite the printed page, section, figure or table. Cite each side when sources disagree.

## 2. Check the records

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-validation.txt
.\.venv\Scripts\python.exe tools/validate.py --reports
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

The validator checks the whole catalogue. Fix the named file and field for schema errors. For a broken ID, check which record the source actually identifies before changing the link. See [catalogue schema](../schemas/catalogue.schema.json) for required fields and allowed values. Each valid scenario gets `reviews/SCN-xxxx/review.md` and `review.json`. A matching previous AI review is kept on regeneration. If the reviewed catalogue packet changes, the regenerated report marks source review as pending.

## 3. Request independent source review

Keep `OPENAI_API_KEY` in your environment or in the ignored root `.env`. The optional settings are `VALIDATION_MODEL` (default `gpt-5-mini`) and `VALIDATION_API_BASE_URL` (an endpoint compatible with the OpenAI Responses API and structured outputs). A model also needs PDF input support when reviewing a PDF.

```powershell
.\.venv\Scripts\python.exe tools/validate.py SCN-0004 --source "C:\path\to\thesis.pdf"
```

Use `--source` again for additional local artifacts associated with the primary source. A manifest can associate each artifact with a different registered source ID. The manifest is JSON with `scenario_id` and an `artifacts` array. Each entry has `source_id` and a `kind`.

| Kind | How to supply evidence |
| --- | --- |
| `local` | Set `path` relative to the manifest or use an absolute path. Use PDFs or UTF-8 text such as Python, YAML, XML, TOML, Markdown, CSV, JSON, or HTML. |
| `public_document` | Register a public HTTPS documentation URL in the evidence registry. The reviewer receives the readable text of that page. Use a local PDF for a publication whose layout or figures matter. |
| `git` | Register the Git repository URL and full commit in the evidence registry. Set a repository-relative `path` and pass `--git-checkout` with a clone containing that commit. Optional `line_start` and required `line_end` for an excerpt let you select lines from large text files and gzip-compressed text. |
| `archive` | Register a ZIP as a `source_archive` with a `urn:sha256:` source identifier. Set `path` to the member name and pass `--archive` with the ZIP. The validator checks the archive hash and reads selected text members directly. |

The SCN-0001 pilot has a [source manifest](../reviews/SCN-0001/sources.json). It selects code, configuration, lockfile excerpts, data excerpts and public documentation.

```powershell
git clone https://gitlab.com/mosaik/examples/mosaik-demo.git "$env:TEMP\mosaik-demo-review"
.\.venv\Scripts\python.exe tools/validate.py SCN-0001 --manifest reviews/SCN-0001/sources.json --git-checkout "$env:TEMP\mosaik-demo-review"
```

Run source review only for artifacts you are authorized to send to the configured API. The command sends the selected evidence in two requests and can incur charges. The first request receives the source material alone. The second receives the source, independent extraction and selected catalogue records. The report records artifact hashes, unavailable sources and the model's findings. Keep private source files outside the repository. Review report contents before sharing them.

## 4. Resolve findings and open a pull request

Read the report's missing, contradicted, uncertain, and human-question items first. Open the source at the cited locator. Correct the catalogue when the source warrants it, or retain the gap with a short rationale. Model output is advisory. A locator can be imprecise even when the finding sounds plausible.

The report derives `structurally_validated` after local checks and `evidence_checked` after a completed source review with a consistent source identity. These statuses describe work performed. A human can set `review_status: human_reviewed` or `accepted` in the scenario file with a `human_review` mapping containing `reviewer`, `date` and `note`. Existing records without a declared status are treated as `draft`. Collection, evidence and runtime statuses retain their separate meanings. Accept a scenario after the important claims and unresolved limitations have been reviewed and the PR checks pass.

When ready, make a topic branch, stage the specific scenario, registry and report files you intend to share, and review the staged diff. The following example assumes the changes are ready to commit and you are on your local base branch.

```powershell
git switch -c review/scn-0004
git status --short
git add -- scenarios/SCN-0004 reviews/SCN-0004
git diff --cached --check
git diff --cached
git commit -m "Review scenario SCN-0004"
git push -u origin review/scn-0004
```

Stage any associated model, publication, software, evidence and catalogue changes when they are part of the PR. Open a pull request in GitHub and include the report and outstanding questions for the reviewer. GitHub Actions runs the local checks and tests with read-only repository access and publishes logs and review indexes under **Actions → Scenario validation → Artifacts**. Enable GitHub Actions if the repository has it disabled. The workflow requires no API secret. Run API review separately from VS Code and include the reviewed reports in the PR. Approval and merge remain human actions.

## Share a review index

The Markdown report is the review index. When a revision is available on GitHub, use `--github-repo OWNER/REPO --github-revision COMMIT_SHA` to generate links for that revision. Use a custom `--output-dir` for standalone indexes. The commit must contain the reviewed files. For a private repository, give the recipient access or share the approved report and source artifacts through an authorized channel.
