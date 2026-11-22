# SCN-0001 — mosaik Smart Grid Demo

The official mosaik demo shows how to assemble and coordinate a co-simulation of a small electrical distribution network, residential electricity demand and photovoltaic (PV) generation. The catalogue describes the Python entry point `demo.py` at revision `74e2e1b8e53a3bfa1cdbba8897c7e8cd5d23b1e8`. The upstream README presents it as a software demonstration. [Pinned README, EVD-0001](https://gitlab.com/mosaik/examples/mosaik-demo/-/blob/74e2e1b8e53a3bfa1cdbba8897c7e8cd5d23b1e8/README.md#L1-18)

## System and components

| Simulator alias | Software and model | Entities and role |
| --- | --- | --- |
| `PyPower` | `mosaik-pypower` with PYPOWER, distribution network `MOD-0001` | One `Grid` with one reference bus, 38 PQ buses, one transformer and 37 line branches. A power-flow calculation determines voltages and power flows from the network and applied loads. A reference bus provides the voltage reference. PQ buses accept specified active and reactive power. |
| `HouseholdSim` | `mosaik-householdsim`, profile-based `HouseModel` (`MOD-0003`) | One `ResidentialLoads` parent and 37 `House` entities, one for each node in the selected profile-file list. The file declares 60 load profiles. |
| `CSV` | `mosaik-csv`, prescribed PV profile `MOD-0002` | Twenty `PV` entities replay the same timestamped active-power series from `pv_10kw.csv`. The source of the values is unknown. |
| `WebVis` | `mosaik-web` | One `Topology` entity consumes selected values for browser visualization. |
| `DB` | `mosaik-hdf5` | One `Database` entity records connected time series in `demo.hdf5`. |

The grid case uses a 10 MVA base. The participation records specify the models, simulator launch methods and settings for this particular run. The model registry identifies the network case, PV series and household model so other scenarios can refer to those same definitions. [Scenario setup, EVD-0005](https://gitlab.com/mosaik/examples/mosaik-demo/-/blob/74e2e1b8e53a3bfa1cdbba8897c7e8cd5d23b1e8/demo.py#L47-81) · [Grid data, EVD-0008](https://gitlab.com/mosaik/examples/mosaik-demo/-/blob/74e2e1b8e53a3bfa1cdbba8897c7e8cd5d23b1e8/data/demo_lv_grid.json) · [Dependency and data evidence, EVD-0006 and EVD-0009–0011](../../evidence/evidence.yaml)

## Co-simulation and data flows

Mosaik starts the grid, household and CSV simulators in the Python process and launches the browser and HDF5 components as external processes. The scenario creates entities (individual instances of models or output components) and connects their named attributes. The mosaik scheduler uses those connections to decide when components can advance and routes data between them. [Launch configuration, EVD-0003](https://gitlab.com/mosaik/examples/mosaik-demo/-/blob/74e2e1b8e53a3bfa1cdbba8897c7e8cd5d23b1e8/demo.py#L9-44) · [Scheduler documentation, EVD-0017](https://mosaik.readthedocs.io/en/3.6.0/scheduler.html)

| Source → destination | Exchange |
| --- | --- |
| House → PQ bus | Active power `P_out` → `P` in watts. During setup the script reads each house's `node_id` to find its bus. |
| PV → selected grid node | Active power `P` → `P` in watts. With seed 23, the helper distributes the 20 connections across eligible grid children whose entity IDs contain `node`, as evenly as possible. |
| House and PV → HDF5 and browser | House `P_out` and PV `P`, each under its original attribute name. |
| Reference and PQ buses → HDF5 | `P`, `Q`, `Vl`, `Vm`, `Va` (active and reactive power, nominal voltage, voltage magnitude and voltage angle). |
| Transformers and line branches → HDF5 | `P_from`, `Q_from`, `P_to`, `P_from` as written. The call repeats `P_from`. The adapter exposes `Q_to`, which the scenario never requests. |
| Reference and PQ buses → browser | Both `P` and `Vm` are connected. The display uses `P` for the reference bus and `Vm` for PQ buses. |

The interaction records label exchanges into the grid as simulation coupling, exchanges into HDF5 as result recording, and exchanges into the browser as visualization.

The power-flow adapter sums the inputs received for each attribute at a bus before solving. The configured household and PV feeds supply active power. Sources feed the grid and output components, and the grid feeds those outputs. [Coupling and output wiring, EVD-0005–0007](https://gitlab.com/mosaik/examples/mosaik-demo/-/blob/74e2e1b8e53a3bfa1cdbba8897c7e8cd5d23b1e8/demo.py#L60-142) · [Grid interface, EVD-0010](../../evidence/evidence.yaml)

## Configuration and demonstrated outputs

The repository script starts at `2014-01-01 00:00:00` and runs unpaced for 31 simulated days with a one-second mosaik time unit and an exclusive end time of 2,678,400 seconds. Power flow and household load updates occur every 15 minutes. The PV input has one-minute samples. The browser and HDF5 components each have a 60-second step setting. The bundled `pv_30kw.csv` is an alternative data file. The checked-in entry point selects `pv_10kw.csv`. The project declares Python 3.12 or newer, and the reviewed lock pins mosaik 3.6.0 and the component versions listed in the scenario record. [Runtime settings, EVD-0003 and EVD-0005](https://gitlab.com/mosaik/examples/mosaik-demo/-/blob/74e2e1b8e53a3bfa1cdbba8897c7e8cd5d23b1e8/demo.py#L29-77) · [Lockfile, EVD-0004](https://gitlab.com/mosaik/examples/mosaik-demo/-/blob/74e2e1b8e53a3bfa1cdbba8897c7e8cd5d23b1e8/uv.lock) · [Profile evidence, EVD-0006, EVD-0009, EVD-0011–0012 and EVD-0014](../../evidence/evidence.yaml)

The script configures an interactive browser view on port 8000 and HDF5 time-series storage. OFFIS describes three hosted variants that loop over April, August and December 2014, with medium, high and low PV active power, respectively. These are properties of the hosted demonstration. Its deployment revision and exact profile-to-variant mappings are unknown. [Output configuration, EVD-0007](https://gitlab.com/mosaik/examples/mosaik-demo/-/blob/74e2e1b8e53a3bfa1cdbba8897c7e8cd5d23b1e8/demo.py#L64-131) · [Hosted live demo, EVD-0002](https://mosaik.offis.de/live-demo/)

## Scientific context and limits

The reviewed materials establish an instructional purpose. A 2015 master's thesis by Jan Sören Schwarz reports two evaluation scenarios derived from an earlier mosaik demo in section 5.1.1. The thesis is related methodological context. A scientific evaluation tied to the reviewed January configuration remains unestablished. [Thesis, EVD-0013](https://mosaik.offis.de/downloads/AdaptiveStateEstimationInOdysseus.pdf#page=77)

The catalogue is based on static inspection of the script, bundled data and locked component sources. Numerical results and runtime behavior were left unverified. The upstream README mentions `requirements.txt`, which is absent from the pinned tree. The dependency evidence comes from `pyproject.toml` and `uv.lock`. The original provenance and representativeness of the household and PV profiles, the intended timezone of their timestamps, and the motivation for the repeated branch attribute remain unresolved. [Evidence register](../../evidence/evidence.yaml)
