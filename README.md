# Co-Simulation Scenario Library

This library documents co-simulation scenarios from scientific publications and source code, with an initial focus on mosaik. Each entry describes what was coupled, how the components exchanged data, and where to check those claims.

## Start with a scenario

Open the [Level 1 scenario overview](catalogue/overview.md) to compare domains, components, research objectives, and original sources. The [CSV catalogue](catalogue/scenarios.csv) is available for spreadsheet use. If you're new to co-simulation, start with the official mosaik demo.

| Scenario | Description | Review |
| --- | --- | --- |
| `SCN-0001` | [Official mosaik smart-grid demo](scenarios/SCN-0001/description.md) | [Report](reviews/SCN-0001/review.md) |
| `SCN-0002` | [Urban multi-energy scalability benchmark](scenarios/SCN-0002/description.md) | [Report](reviews/SCN-0002/review.md) |
| `SCN-0003` | [Distribution-grid flexibility control laboratory](scenarios/SCN-0003/description.md) | [Report](reviews/SCN-0003/review.md) |
| `SCN-0004` | [Two-subgrid SCADA monitoring testbed](scenarios/SCN-0004/description.md) | [Report](reviews/SCN-0004/review.md) |
| `SCN-0005` | [mosaik smart-grid demo with ontology export](scenarios/SCN-0005/description.md) | [Report](reviews/SCN-0005/review.md) |
| `SCN-0006` | [Electrification of residential end-users](scenarios/SCN-0006/description.md) | [Report](reviews/SCN-0006/review.md) |
| `SCN-0007` | [Electrification of industrial prosumers](scenarios/SCN-0007/description.md) | [Report](reviews/SCN-0007/review.md) |
| `SCN-0008` | [District heating peak reduction under varying supply temperatures](scenarios/SCN-0008/description.md) | [Report](reviews/SCN-0008/review.md) |
| `SCN-0009` | [EV charging and transformer loading in a photovoltaic-rich low-voltage grid](scenarios/SCN-0009/description.md) | [Report](reviews/SCN-0009/review.md) |

## Follow the records

Each scenario has four files. Here is the route through `SCN-0001`. The same layout applies to the other entries.

1. **Read the description** to understand the purpose, setup, and limitations. [description.md](scenarios/SCN-0001/description.md)
2. **Open the scenario metadata** for the framework, settings, source IDs, and any primary or related publication. [scenario.yaml](scenarios/SCN-0001/scenario.yaml)
3. **Find the components and their roles.** The participation records show which models and software the scenario uses and what each component does in this setup. [participations.yaml](scenarios/SCN-0001/participations.yaml)
4. **Trace the data flows.** The interaction records identify the sender, receiver, exchange purpose, and attributes or quantities where known. [interactions.yaml](scenarios/SCN-0001/interactions.yaml)
5. **Check the evidence and review status.** Look up an `EVD-xxxx` ID for the original source and the relevant page, section, or code lines. The review report shows which checks ran and which questions are still open. [Evidence register](evidence/evidence.yaml) · [SCN-0001 review](reviews/SCN-0001/review.md)

## Look up a model, package, or publication

| ID | Where to look | What it identifies |
| --- | --- | --- |
| `MOD-xxxx` | [Model registry](models/) | A reusable definition, such as a grid case, prescribed time series, or controller design. |
| `SW-xxxx` | [Software registry](software/software.yaml) | A software package or framework. Scenario records hold the versions used where known. |
| `PUB-xxxx` | [Publication registry](publications/) | A paper, thesis, or other publication. Follow the scenario's explicit publication link, since one publication can describe several scenarios. |
| `EVD-xxxx`, `SRC-xxxx` | [Evidence register](evidence/evidence.yaml) | A claim and its locator, or the original source it refers to. |

For example, [PUB-0006](publications/PUB-0006.yaml) is the primary publication for both `SCN-0006` and `SCN-0007`. A `null` field marks an unresolved or inapplicable value. Check the surrounding notes and evidence for the reason.

## Contribute or review

New scenarios start at **Level 1**, a source-backed overview of what they study and which components participate. Use the [collection protocol](docs/SCENARIO_COLLECTION_PROTOCOL.md) and regenerate the overview with `python tools/generate_overview.py`. **Level 2** starts on request and uses the [detailed review workflow](docs/SCENARIO_REVIEW_WORKFLOW.md), including independent source review where appropriate. Structural checks, scientific review, and runtime reproduction have separate outcomes.
