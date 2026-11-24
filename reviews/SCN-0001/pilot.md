# SCN-0001 workflow test

The pilot used the official mosaik demo at commit `74e2e1b8e53a3bfa1cdbba8897c7e8cd5d23b1e8`. The [source manifest](sources.json) identifies the exact files and excerpts selected. The [Markdown review](review.md) and [JSON findings](review.json) contain artifact hashes and distinguish automated structural checks from model assessments.

| Check | Result |
| --- | --- |
| Catalogue integrity | Passed for 31 YAML documents and 150 record IDs. The nine SCN-0001 interactions and their evidence references passed relationship checks. |
| Negative tests | Passed for malformed records, including duplicate keys and IDs, missing fields, invalid interaction types, cross-scenario endpoints and missing evidence. |
| Source inputs | Read nine artifacts from the pinned commit, including source, configuration, dependency lock excerpts and dataset excerpts. Retrieved the versioned scheduler documentation. The hosted live-demo endpoint returned HTTP 401. Package implementation files and the linked historical thesis were outside this review batch. |
| Live API review | Both passes completed. The comparison returned structured findings and identified relevant code locations for the run setup, PV input and grid coupling. |
| GitHub workflow | Passed local `actionlint`. GitHub execution awaits a branch or pull request containing the workflow. |
| Runtime | The simulation was left unrun. The pilot does not establish reproducibility. |

## Findings to adjudicate

- **Keep the repeated branch mapping as recorded.** The reviewer suggested changing the repeated `P_from`. The pinned script genuinely repeats it, and `INT-0006` already preserves that source behavior. Any upstream fix would be a separate change. [Pinned demo code, lines 73–74](https://gitlab.com/mosaik/examples/mosaik-demo/-/blob/74e2e1b8e53a3bfa1cdbba8897c7e8cd5d23b1e8/demo.py#L73-74)
- **Keep input provenance and timezone unresolved.** The scenario already records these gaps. The reviewed samples do not determine the origin of the profiles or the timezone of their timestamps.
- **Treat the hosted variants as an evidence gap for this run.** The unavailable page prevents this reviewer from checking the variant descriptions directly. The pinned repository does not establish a mapping from hosted variants to input files.
- **Keep solver behavior and HDF5 internals scoped to their evidence.** The dependency lock establishes versions. Exact runtime behavior and storage layout need their own evidence.

The scenario and its evidence records were preserved. The generated status records completed evidence review for the supplied artifacts. Human approval is pending.
