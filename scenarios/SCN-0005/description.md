# SCN-0005 — mosaik smart-grid demo with ontology export

The supplied `mosaik-scenario-planning.zip` contains a code-defined scenario based on the smart-grid demo. The scenario configures grid power flow, household demand, and PV replay, then exports the instantiated configuration for ontology-based planning checks. The ZIP is identified by SHA-256 `e3749b8800868abfd761cffe77515dc7d2193109caec3ce071ed30a4ea3f405f`. Its upstream repository URL and commit could not be established. [Evidence register](../../evidence/evidence.yaml)

## What the code configures

- `eval_mosaik_demo/demo_eval.py` sets a January 1, 2014 input start, a one-day horizon (86,400 seconds), and random seed 23. It creates 20 PV entities from `pv_10kw.csv`, loads the household profiles, and starts the grid with a 900-second step. The HDF5 recorder has a 60-second step.
- Houses send `P_out` to the matching grid bus as `P`. PV entities send `P` to grid nodes selected by the scenario's seeded random helper. Houses, PVs, buses, and branches also feed HDF5. The branch wiring includes `Q_to`. Web, SQL, and FMI examples do not run in the active scenario.
- The grid JSON and PV series match the reviewed SCN-0001 inputs after line-ending normalization. The compressed household profile bytes also match. The locked household package exposes the scenario's legacy import as an alias of the implementation already recorded in MOD-0003. The same model IDs are therefore reused.
- Calling `demo_eval.main()` defaults to running the simulation after exporting RDF/XML, N-Triples, and JSON-LD. The dissertation workflow calls it with `run=False`, then invokes ontology checks. This catalogue review inspected the code and left it unexecuted.

## What the DFG files establish

`dfg_process.py` builds planning metadata for aims, hypotheses, and evaluation criteria. The archive includes the workbooks but its DFG configuration refers to `20201120_Integrated_InformationModel.xmind`, which is absent. The archive README cites Adelt et al. for this planning workflow. The chapter documents two examples separately catalogued as [SCN-0006](../SCN-0006/description.md) and [SCN-0007](../SCN-0007/description.md). Their executable configurations were not established from the archive. [Related chapter](https://doi.org/10.1007/978-3-031-34920-1_38)

## Benchmark use

This scenario and SCN-0001 make a useful comparison for extraction. Check that the reviewer distinguishes the one-day horizon from SCN-0001's 31 days, keeps each script's HDF5 branch attributes intact, and excludes inactive visualization wiring. These checks exercise fidelity to the source. Numerical reproducibility would require a separate run and output comparison. [Source locators and claims](../../evidence/evidence.yaml)

## Reuse terms and evidence gaps

| Artifact | What the sources establish |
| --- | --- |
| Demo directory in the supplied ZIP | `eval_mosaik_demo/LICENSE.txt` contains the **GNU LGPL version 2.1** text. The archive-level terms and the exact coverage of this file across the demo and bundled data remain unresolved. `EVD-0070` |
| Bundled grid JSON, PV CSV files and compressed household profiles | The inspected archive contains no separate data license statement. Terms specific to these files remain unresolved. `EVD-0071` |
| Household model implementation in `mosaik-householdsim` 2.2.0 | The lock-matched package wheel declares **MIT**. This evidence applies to the implementation artifact. `EVD-0072` |
| Grid solver adapter in `mosaik-pypower` 0.9.0 | The lock-matched wheel declares **MIT**. This evidence applies to the adapter package. `EVD-0073` |
| PV profile reader in `mosaik-csv` 2.0.1 | The lock-matched wheel ships the **GNU LGPL version 2.1** text. Its free-text license metadata says `UNKNOWN`, and its classifier says LGPLv2. This evidence applies to the reader package. `EVD-0074` |

See the [evidence register](../../evidence/evidence.yaml) for the archive paths and package locations. Package terms do not establish rights for separate input data.
