# SCN-0005 review findings checked against the archive

The [archive-only API report](archive-review.md) is advisory. It predates the link to Adelt et al. The following checks use the ZIP registered as `SRC-0018`.

| Finding | Source check and disposition |
| --- | --- |
| Active simulators and exchanges | `eval_mosaik_demo/demo_eval.py:100–136,205–211` supports four active simulators, household and PV coupling, and the recorded HDF5 mappings, including `Q_to`. |
| Automatic addition of matched components | `diss_process.py:70–82` performs the matching query. The code that adds the selected models is gated by `choose_option`, which is set to `False`. The catalogue makes no claim of automatic addition in this run. |
| Runtime data in the RDF export | `eval_mosaik_demo/demo_eval.py:71–87` builds and exports the scenario ontology before its optional simulation call. `diss_process.py:87` passes `run=False`. Runtime traces were unverified, and the catalogue makes no claim that they are exported. |
| DFG workbook | `xmind/xmind_im_export_dfg.config:6–9` names the integrated XMind workbook. The ZIP member listing confirms that it is absent. This gap is already recorded in the scenario description. |

The review did not establish a second configured scenario or a reason to change the current mappings. Human approval and runtime verification are pending.
