# SCN-0001 — mosaik Smart Grid Demo

## Deterministic validation

Catalogue checks: **passed** (46 YAML files, 203 IDs).
Review status: `evidence_checked`. Declared human workflow status: `draft`. Runtime status: `not_run`.

Catalogue packet SHA-256: `05691b2db4f67badb79357427b6f6e2affac944387345e79a136c770d0dd9429`.

## Review index

- [scenarios/SCN-0001/interactions.yaml](../../scenarios/SCN-0001/interactions.yaml)
- [scenarios/SCN-0001/participations.yaml](../../scenarios/SCN-0001/participations.yaml)
- [scenarios/SCN-0001/scenario.yaml](../../scenarios/SCN-0001/scenario.yaml)
- [scenarios/SCN-0001/description.md](../../scenarios/SCN-0001/description.md)
- [models/MOD-0001.yaml](../../models/MOD-0001.yaml)
- [models/MOD-0002.yaml](../../models/MOD-0002.yaml)
- [models/MOD-0003.yaml](../../models/MOD-0003.yaml)
- [publications/PUB-0001.yaml](../../publications/PUB-0001.yaml)
- [software/software.yaml](../../software/software.yaml)
- [evidence/evidence.yaml](../../evidence/evidence.yaml)

## Original sources and review inputs

- SRC-0001 [mosaik-demo (official repository)](https://gitlab.com/mosaik/examples/mosaik-demo) at `74e2e1b8e53a3bfa1cdbba8897c7e8cd5d23b1e8`
- SRC-0002 [mosaik Live-demo](https://mosaik.offis.de/live-demo/)
- SRC-0003 [mosaik](https://pypi.org/project/mosaik/3.6.0/#files) at `3.6.0`
- SRC-0004 [mosaik-csv](https://pypi.org/project/mosaik-csv/2.0.1/#files) at `2.0.1`
- SRC-0005 [mosaik-householdsim](https://pypi.org/project/mosaik-householdsim/2.2.0/#files) at `2.2.0`
- SRC-0006 [mosaik-pypower](https://pypi.org/project/mosaik-pypower/0.9.0/#files) at `0.9.0`
- SRC-0007 [mosaik-web](https://pypi.org/project/mosaik-web/0.5.0/#files) at `0.5.0`
- SRC-0008 [mosaik-hdf5](https://pypi.org/project/mosaik-hdf5/0.5.2/#files) at `0.5.2`
- SRC-0009 [Adaptive State Estimation in Odysseus](https://mosaik.offis.de/downloads/AdaptiveStateEstimationInOdysseus.pdf)
- SRC-0010 [mosaik scheduling and simulation execution](https://mosaik.readthedocs.io/en/3.6.0/scheduler.html) at `3.6.0`
- A1 (SRC-0001) README.md — supplied. 9bff828749307a41257162e85b040d3be0ec2ef7f05f7c3ecc99d33ec8a62728
- A2 (SRC-0001) demo.py — supplied. c4cd5da5bcb6d5aa80d61116d5c6c6afc90e1f746d067db7104ec35021908ac6
- A3 (SRC-0001) pyproject.toml — supplied. 4b47d8fdeb6a703de056de2aedffae80a20aeb4b73d365e2e9daf2a3d32bb8c9
- A4 (SRC-0001) uv.lock lines 104–232 — supplied. 75a33b9f616308144b31bacf46c59e45db441d8e8fa38d59385e8f5ad1dc03fe
- A5 (SRC-0001) uv.lock lines 337–344 — supplied. 75a33b9f616308144b31bacf46c59e45db441d8e8fa38d59385e8f5ad1dc03fe
- A6 (SRC-0001) data/demo_lv_grid.json — supplied. e00d453729d58d3b19a8522697aae62386a62539d64b57b1b4f323fff2e686f4
- A7 (SRC-0001) data/pv_10kw.csv lines 1–5 — supplied. ef22daed525e519b2eb0f7b6a4a2434519be41ff934aa2d718e997c01f84c510
- A8 (SRC-0001) data/pv_30kw.csv lines 1–5 — supplied. 4f93e6d4aa15eb5aa8baf2d6fbc85aff34a6db29260632ea4fdfad83eef260e8
- A9 (SRC-0001) data/profiles.data.gz lines 1–10 — supplied. 7763f589a4ede25cd6f2b57da890b05fa244835b42a74f9e2f42d1f6e94db7f2
- A10 (SRC-0002) https://mosaik.offis.de/live-demo/ — unavailable. HTTP Error 401: Unauthorized
- A11 (SRC-0010) https://mosaik.readthedocs.io/en/3.6.0/scheduler.html — supplied. 1791bb534e54075861d0e0e19cdae605311eb7c329b952f184b9fe9fcbede9d8

## AI-assisted evidence review

Status: **completed**.
Reviewer: `gpt-5-mini`. Source assessment: `consistent`.

The findings require human judgment. The review does not approve the scenario.

- Time-series files and profiles shown only as excerpts; full PV and profile data are not provided so actual generation/load time series over 31 days cannot be verified (A7 lines 1–5; A9 lines 1–10).
- No runtime execution traces, logs or produced output files (demo.hdf5, web snapshots) are provided, so actual runtime behavior, convergence and data timestamps are unverified.
- Simulator internal implementations are external dependencies (mosaik_components.* and mosaik-* packages). The repository shows how they are invoked but not their internal numerical or control behaviour (demo.py lines 49–51; pyproject.toml lines 7–13).
- uv.lock provides pinned upstream package versions and upload timestamps, but those locked artifacts are external and the lock does not prove identical binaries will be used in another environment (uv.lock lines 104–232, 337–344).
- Entity runtime identifiers (full eids) and resulting mapping counts are only inferred from code; the exact runtime eids are not enumerated in the supplied artifacts (demo.py lines 134–142).

### Needs evidence (2)

- **Source/origin of the PV time series in pv_10kw.csv (how values were produced) is unknown**
  - Catalogue: participations/ PART-0002.configuration.original_profile_source
  - Evidence: A7 data/pv_10kw.csv lines 1–5 (excerpt)
  - Assessment: CSV file shows timestamps and P values but contains no provenance metadata describing how the series was generated.
  - Suggested action: Add provenance metadata (source, generation method, units & timezone) to the CSV header or repository documentation.
- **Hosted live demo reports specific monthly PV power levels (April/medium, August/high, December/low); mapping to repo configuration is unknown**
  - Catalogue: scenario.yaml:live_demo.variants
  - Evidence: EVD-0002
  - Assessment: The reviewer did not supply a usable artifact locator. The catalogue references a hosted live-demo page (EVD-0002) that describes variants, but the repository does not include configuration mapping these variants to specific data files or revisions.
  - Suggested action: Do not assume the hosted variant mappings reflect this commit. Add explicit variant mapping metadata if the repository supports those variants.

### Missing metadata (2)

- **Time zone for profiles and CSV timestamps is unspecified**
  - Catalogue: profiles.data.gz:timezone
  - Evidence: A9 profiles.data.gz decompressed lines 1–6
  - Assessment: profiles.data.gz metadata includes start_date and resolution but no timezone; demo.py does not set an explicit timezone.
  - Suggested action: Document the intended timezone for all input time series (profiles and CSV) or include timezone-aware timestamps.
- **Branch HDF5 connection repeats 'P_from' and omits 'Q_to' that adapter exposes**
  - Catalogue: demo.py:branch_hdf5_connection
  - Evidence: A2 demo.py lines 73–75
  - Assessment: connect_many_to_one call lists 'P_from', 'Q_from', 'P_to', 'P_from' (P_from repeated). The adapter (per catalogue) exposes Q_to which is not requested here.
  - Suggested action: Fix the attribute list to include intended attributes and remove duplicates (e.g., replace duplicate 'P_from' with 'Q_to' if appropriate).

### Model identity concern (1)

- **PYPOWER underlying solver is an external dependency and its exact runtime behaviour depends on that package version**
  - Catalogue: participations/ PART-0001.dependency_software_ids
  - Evidence: A4 uv.lock lines 201–214; uv.lock lines 337–344 (pypower entry)
  - Assessment: uv.lock pins pypower 5.1.19 and mosaik-pypower 0.9.0; numerical behaviour and convergence criteria are determined by those external packages, not by files in this repo.
  - Suggested action: If precise numerical reproducibility is required, include or reference the exact solver configuration and any solver options used at runtime.

### Human question (1)

- **Are HDF5 datasets organized with clear entity/attribute naming and checksum/metadata to detect corruption?**
  - Catalogue: No existing field
  - Evidence: A2 demo.py lines 65–74
  - Assessment: demo.py configures HDF5 writing but the exact dataset naming schema and integrity checks depend on mosaik-hdf5 implementation; the repo does not include produced HDF5 or explicit integrity checks.
  - Suggested action: Add a short note or example HDF5 structure and enable checksums or metadata writing via mosaik-hdf5 configuration if supported.

### Supported (7)

- **Simulation start is 2014-01-01 00:00:00**
  - Catalogue: scenario.yaml:configuration.input_start
  - Evidence: A2 demo.py line 29
  - Assessment: demo.py defines START = '2014-01-01 00:00:00'.
  - Suggested action: Review the cited evidence.
- **Simulation end is 31 days (END = 31 * 24 * 3600)**
  - Catalogue: scenario.yaml:configuration.end_time_seconds_exclusive
  - Evidence: A2 demo.py lines 30–31
  - Assessment: END is set to 31 * 24 * 3600 in demo.py.
  - Suggested action: Review the cited evidence.
- **PyPower (mosaik-pypower) used for grid, started with step_size=15*60 seconds**
  - Catalogue: participations/ PART-0001
  - Evidence: A2 demo.py line 49 (start call) and lines 20–23 (sim_config)
  - Assessment: demo.py starts 'PyPower' with step_size=15*60; sim_config contains PyPower launch info.
  - Suggested action: Review the cited evidence.
- **CSV adapter provides PV time series; demo selects data/pv_10kw.csv and creates 20 PV entities**
  - Catalogue: participations/ PART-0002
  - Evidence: A2 demo.py lines 51, 58; data/pv_10kw.csv excerpt A7 lines 1–5
  - Assessment: demo.py starts CSV with datafile PV_DATA and calls pvsim.PV.create(20); pv_10kw.csv header and sample shown.
  - Suggested action: Review the cited evidence.
- **HouseholdSim instantiates ResidentialLoads and houses are connected to grid nodes by node_id**
  - Catalogue: participations/ PART-0003
  - Evidence: A2 demo.py lines 54–57 and 139–142 (connect_buildings_to_grid)
  - Assessment: ResidentialLoads children used as houses; world.get_data retrieves 'node_id' and world.connect links house P_out to bus P.
  - Suggested action: Review the cited evidence.
- **Grid definition includes a REF bus, 38 PQ buses, one transformer and 37 branches on a 10 MVA base**
  - Catalogue: data/demo_lv_grid.json
  - Evidence: A6 data/demo_lv_grid.json lines 1–46 (buses, trafo) and 47–85 (branches)
  - Assessment: JSON shows 'base_mva':10, listed buses including 'REF' and many 'PQ', one 'trafo' and 37 branch entries.
  - Suggested action: Review the cited evidence.
- **PV placement is randomized but deterministic due to random.seed(23)**
  - Catalogue: demo.py:random_seed
  - Evidence: A2 demo.py lines 40 and 62
  - Assessment: random.seed(23) is set before connect_randomly is used to assign PVs to nodes, making placement repeatable for the seed.
  - Suggested action: Review the cited evidence.
