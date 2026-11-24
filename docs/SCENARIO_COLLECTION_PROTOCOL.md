# Scenario collection protocol

Use this workflow to document co-simulation scenarios from publications, the mosaik Ecosystem page, and repositories. A scenario is a particular setup used to answer a research question or demonstrate a method. A single publication may describe several scenarios, and several sources may document the same scenario.

## Level 1 — Scenario Overview (default)

Collect at Level 1 unless the maintainer explicitly requests Level 2. The aim is to build a broad inventory across domains.

1. Identify the scenario and check for an existing ID. Record `collection_level: 1`, its title, general domain, a one- or two-sentence purpose in `research_objective` or `technical_purpose`, and the original source IDs in `scenario.yaml`. Save the publication citation and DOI or PDF URL, repository and known revision, and relevant documentation in the existing registries. Use `null` for a primary publication when none has been identified.
2. Write a meaningful, source-supported `description.md`. Explain what is being investigated or demonstrated and how the named components contribute. The one- or two-sentence limit is for the shareable overview table.
3. In `participations.yaml`, give each reported component an ID, its source-reported name and evidence IDs. Add a basic role when the source provides one. Model and software IDs and detailed configuration are optional. If components are unavailable, use an empty list with a note that explains the gap. `interactions.yaml` may be omitted.
4. Record useful extra details in the description or evidence notes and flag gaps where a future metadata field may help. Add the CSV catalogue row and run `python tools/generate_overview.py`, which checks the catalogue and refreshes the [shareable overview](../catalogue/overview.md). A routine Level 1 collection pass needs no separate API review, simulation run, or pull request.

## Level 2 — Detailed Investigation (on request)

Start from the existing scenario ID and its saved sources. Apply the detailed steps below, add model identities and interactions as the evidence allows, and use `collection_level: 2` when the record meets the detailed checks. Existing records without a level field continue to use those checks. Detailed entries also appear in the Level 1 overview.

### 1. Identify the source and scenario

1. Read the publication's methods, diagrams and results. Inspect cited supplements, code and data when available. Record the publication in `publications/PUB-xxxx.yaml` and register it and other reviewed sources in `evidence/evidence.yaml`. Use a DOI or stable URL and record any known version.
2. Identify the system, research objective and boundaries of the scenario. Give a materially different setup its own scenario record when the source describes it independently. Keep parameter sweeps or repeated runs together when the source treats them as variants of one setup. Record the rationale when the boundary is ambiguous.
3. Reuse an existing ID when the identity is established. Use a new ID for a distinct record.

### 2. Write a description a reader can use

Create `scenarios/SCN-xxxx/description.md` and `scenario.yaml`. Explain the research question or stated purpose, the system and its boundary, why components were coupled, what each component does, and how information moves between them. Summarize the studied conditions, reported outcomes and limitations at the level the source supports. Attribute findings to the publication and distinguish results obtained in the study from outputs the setup could produce. Cite evidence for claims and disclose important gaps in the source.

### 3. Describe the participants

Record each identifiable component and its scenario role in `participations.yaml`. A **model** represents a system or supplies prescribed behavior, such as a time series. A **simulator** runs or serves that representation. **Software** is the package or tool providing the implementation. A **participation** is the use of a component in this scenario. An **entity** is an instance, such as a house or a bus.

Use `models/` for independently identifiable definitions and `software/software.yaml` for packages. Create a model ID only when evidence establishes what the definition is. For a reported model with uncertain identity, retain its reported name in the participation, set `model_id: null` and explain the uncertainty. An output component such as a recorder can have a participation with no system model. A file of PV power values establishes a prescribed input profile. Identifying the physical or mathematical model that produced those values requires separate evidence.

### 4. Record the exchanges

Use `interactions.yaml` for exchanges supported by the sources. Identify the sending and receiving participation IDs and record the reported direction, quantities or signals, attribute mappings and units where known. Preserve source names, ordering and repeated mappings when they carry evidence about what was configured. Explain anomalies in a note.

| `interaction_type` | Meaning |
| --- | --- |
| `simulation_coupling` | One component supplies input used by another component's simulation or control logic. |
| `result_recording` | Data goes to a recorder, file writer or other storage component. |
| `visualization` | Data goes to a display or plotting component. |

Classify each flow by what the receiver does with the data. If the purpose or direction is unclear, describe the reported relationship and the gap in the narrative. Where the endpoints and direction are known but the type is unclear, use `interaction_type: null` and explain the gap. An empty interaction list with a review status and explanatory note can represent a source that provides no usable wiring details.

### 5. Preserve evidence and uncertainty

Connect material claims to evidence IDs. Give each evidence entry a source ID, a locator and an evidence status. For a publication, use the page, section, figure, table or listing. For code or data, record the commit or version, path and relevant lines or data location when available.

- Use `explicitly_reported` for claims stated by the source and `verified_from_code` for claims confirmed from inspected code or data.
- Label a reasoned interpretation `inferred`, cite the evidence and explain the reasoning. Keep unestablished claims marked `unknown` when recording the gap.
- Use YAML `null` for a required field whose value is unknown, with a note explaining whether the source omits it, the artifact could not be accessed, or the information is inapplicable. Omit optional details when unavailable. If sources disagree, cite each and say which publication case or code revision the record describes.

### Detailed metadata for a publication-based scenario

This is a collection checklist for the existing files. Each required topic needs a supported value or an explicit account of the gap where indicated.

| Record | Minimum required content |
| --- | --- |
| `scenario.yaml` | Unique scenario ID, title, record type, domain, primary publication ID, source IDs, research objective or stated purpose, collection and verification status, and links to supporting evidence. If the framework is unreported, record it as unknown. |
| `description.md` | Purpose, system and scope, component roles, how the components work together, studied conditions and reported outcomes where available, limitations and evidence links. State when the source leaves any of these topics unresolved. |
| `participations.yaml` | Scenario ID and, for each identifiable participant, a participation ID, reported name, role, evidence IDs and model or software links where established. Keep unresolved identities explicit. If no participants can be identified, explain the gap. |
| `interactions.yaml` | Scenario ID and review status. Each supported exchange has an ID, directed endpoints, a type or explicit unknown, the reported quantity or mapping if available, and evidence IDs. Explain any missing exchanges or details. |
| Publication, evidence and catalogue | Publication identity, citation details and a DOI or stable source URL, claim-level evidence with locators and status, and a catalogue row that agrees with the scenario record. |

Detailed metadata is optional when the publication and supporting artifacts do not provide it. Examples include exact interface names and units, model equations, solver settings, synchronization algorithm, step sizes, entity counts, parameter values, package versions and random seeds. Record these when supported and relevant to interpreting or reproducing the scenario.

### Capture details beyond the current fields

Treat the minimum metadata as a starting point. Look for any source-supported detail that affects how someone understands, compares, reuses, or reproduces the scenario. Examples include model assumptions, limits, initialization, expected outputs, artifact availability, and reuse terms. Consult linked supporting artifacts when available.

For a detail without a dedicated field, use a short observation in the scenario description or the relevant model's `scope`. State what it applies to, what the source establishes, and the evidence ID. Keep scenario-specific settings in the scenario or participation configuration. Record important gaps explicitly.

For licensing, record the stated terms and the artifact they cover, such as a paper, model implementation, FMU, or dataset. Cite the license file or statement and its revision when available. Record a gap when the applicable terms cannot be established and matter for reuse.

### 6. Check the record

Validate YAML and catalogue syntax, uniqueness and resolution of IDs, participation endpoints and their entity types when known, claim-to-evidence links, and agreement among the prose, structured records and catalogue. Check that a reported scientific result can be traced to its publication and that a code configuration is attributed to the reviewed revision. Record the review level and leave runtime verification unresolved when only static inspection was performed.

### Run the validator

From the repository root, install the validation dependency and run the local checks.

```powershell
python -m pip install -r requirements-validation.txt
python tools/validate.py
```

For a source review, set `OPENAI_API_KEY` in the ignored root `.env` file or in your environment. The default reviewer is `gpt-5-mini`. Set `VALIDATION_MODEL` to choose a different model, or `VALIDATION_API_BASE_URL` for an endpoint that supports the Responses API and PDF inputs.

```powershell
python tools/validate.py SCN-0004 --source "C:\path\to\thesis.pdf" > SCN-0004-review.md
```

This sends the selected PDF to the reviewer API twice. The first request extracts claims from the source alone. The second receives the PDF, that extraction and the scenario records with their evidence references. Check the page and section locators in the resulting report before accepting corrections. An API review can incur charges. The script prints findings for review and leaves the catalogue files untouched.

See the [scenario review workflow](SCENARIO_REVIEW_WORKFLOW.md) for review artifacts, additional source types, and the GitHub PR process.
