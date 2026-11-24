# SCN-0009 — EV charging and transformer loading in a photovoltaic-rich low-voltage grid

## Deterministic validation

Catalogue checks: **passed** (63 YAML files, 285 IDs).
Review status: `evidence_checked`. Declared human workflow status: `draft`. Runtime status: `not_run`.

Catalogue packet SHA-256: `f5524a6d47f2b8c7a12295ebbfd738357d71a4a79e511a74ff3aaa2265e6e065`.

## Review index

- [scenarios/SCN-0009/interactions.yaml](../../scenarios/SCN-0009/interactions.yaml)
- [scenarios/SCN-0009/participations.yaml](../../scenarios/SCN-0009/participations.yaml)
- [scenarios/SCN-0009/scenario.yaml](../../scenarios/SCN-0009/scenario.yaml)
- [scenarios/SCN-0009/description.md](../../scenarios/SCN-0009/description.md)
- [models/MOD-0024.yaml](../../models/MOD-0024.yaml)
- [models/MOD-0025.yaml](../../models/MOD-0025.yaml)
- [models/MOD-0026.yaml](../../models/MOD-0026.yaml)
- [publications/PUB-0008.yaml](../../publications/PUB-0008.yaml)
- [software/software.yaml](../../software/software.yaml)
- [evidence/evidence.yaml](../../evidence/evidence.yaml)

## Original sources and review inputs

- Primary publication: [A Modular Simulation Environment for Education and Research in Smart Low-Voltage Grids](https://doi.org/10.1109/SmartGridComm65349.2025.11204608)
- SRC-0021 [Steinhagen et al. (2025), smart low-voltage grid simulation environment](https://doi.org/10.1109/SmartGridComm65349.2025.11204608) at `version_of_record`
- SRC-0022 [Grid-Sim-Builder source repository](https://github.com/Carruthion/grid-sim-builder) at `1a3d59809c93f46d1e5f3adfe941c40d8f49a3ea`
- A1 (SRC-0022) LICENSE — supplied. d8f5186451e89faa825fb4cb586c371e7db0176834852f1876c2a9aff3346671
- A2 (SRC-0022) README.md lines 17–69 — supplied. e657b454ec500c4ab15790a7244f3e7453349f72f06be588b1ccb13eba9e0eca
- A3 (SRC-0022) config/grids/amiro_net/amiro_net.py — supplied. 553cf2b9558246b5d42ca0e583e04cd4a0f01a8cea490da9b6ddc0a07d4f5c80
- A4 (SRC-0022) services/gridserver/src/main.py lines 102–114 — supplied. c5e9fda0b875e1e81bf465855beea9f84f36d70d01138c5aa303f59af547d8ec
- A5 (SRC-0022) services/gridserver/src/main.py lines 600–603 — supplied. c5e9fda0b875e1e81bf465855beea9f84f36d70d01138c5aa303f59af547d8ec
- A6 (SRC-0022) services/gridserver/requirements.txt — supplied. 0d1354403e74f7be69ff79fb7d3e1f065c7dde89ab030fa1228c7b1d899138c1

## AI-assisted evidence review

Status: **completed**.
Reviewer: `gpt-5-mini`. Source assessment: `consistent`.

The findings require human judgment. The review does not approve the scenario.

- Provided snippets do not include full services/gridserver/src/main.py — only selection (lines 102–114 and 600–603) — so initialization of used_model, MQTT/InfluxDB client setup, and implementations of export_state/get_global_timestamp/setter functions are not available for inspection (A4, A5).
- Household CSV/HH list file formats (schema, column names, units) and the contents of demo_load_profiles.tar.gz are not present in supplied artifacts (README references them but does not show schema) (A2).
- Node-RED flows, Grafana dashboards, and Docker Compose service definitions (docker-compose.yml) were not supplied, so live UI/configuration details and service bindings (ports, topics, buckets) cannot be verified.
- requirements.txt lists package names without pinned versions; exact dependency versions used at runtime are unresolved (A6).
- No artifacts supplied for authentication, network security, or MQTT/InfluxDB configuration; operational security posture is therefore unknown.

### Needs evidence (2)

- **Repository is licensed under the MIT License.**
  - Catalogue: license
  - Evidence: A1
  - Assessment: The reviewer did not supply a usable artifact locator. LICENSE file contains the MIT permission grant and disclaimer (full file).
  - Suggested action: Review the cited evidence.
- **The code defaults to AMiRo in published runs and the used_model origin is known.**
  - Catalogue: used_model_default_and_initialization
  - Evidence: A4 services/gridserver/src/main.py, lines 102-114
  - Assessment: The selection branch shows what happens when used_model == 'AMiRo' (lines 109–112), but the supplied fragments do not show where used_model is defined or what default is used at runtime. The catalogue statement that the release 'selects the AMiRo model by default' cannot be fully verified from the supplied lines alone.
  - Suggested action: Provide the portion of main.py (or config) where used_model is set or a default is established, or update the catalogue to mark the default as 'unspecified in supplied code' until verified.

### Missing metadata (2)

- **Household profile CSV schema and demo_load_profiles contents are known.**
  - Catalogue: CSV_schema_and_demo_profiles
  - Evidence: A2 README.md, lines 24-26 and 51
  - Assessment: README says profiles live under config/hh_data/load_profiles and demo_load_profiles.tar.gz must be unpacked, and that profiles are per-household CSVs for load, PV and optional EV charging. However, the actual CSV schema (column headers, timestamp format, units) and the demo tarball contents were not supplied.
  - Suggested action: Attach or point to the hh CSV schema and an example CSV (or include README subsections showing column format) so the catalogue can record precise input formats.
- **Exported telemetry (MQTT topics, InfluxDB measurement names/buckets, fields and tags) are known.**
  - Catalogue: export_state_and_published_schema
  - Evidence: A5 services/gridserver/src/main.py, lines 600-603
  - Assessment: Code calls export_state(...) after runpp, but the implementation of export_state and the exact MQTT topics/InfluxDB schema are not present in supplied artifacts.
  - Suggested action: Supply the implementation of export_state and any configuration files that define MQTT topics and InfluxDB bucket/measurement names so telemetry schemas can be recorded.

### Possible hallucination (1)

- **Catalogue lists household_count = 24 in configuration metadata.**
  - Catalogue: household_count_exactness
  - Evidence: A3 config/grids/amiro_net/amiro_net.py, lines 24-91
  - Assessment: amiro_net.py defines loads and sgens in a pattern that corresponds to 24 household loads and 24 PV sgens; this supports an assertion of 24 households. However, the catalogue's configuration field 'household_count' should be explicitly tied to the code's grouping semantics (e.g., 4 buses × 6 households). If the catalogue treats dummy loads separately from controllable households, clarify the counting method.
  - Suggested action: Document how 'household_count' is derived from the code (e.g., counting unique household load groups vs. individual load entries) to avoid ambiguity.

### Human question (1)

- ****
  - Catalogue: No existing field
  - Evidence: Unresolved
  - Assessment: Where are the implementations of: export_state(), get_global_timestamp(), the setter functions referenced in the README (assets in the loop), and the code that applies per-step CSV values to pandapower sgen/load objects? Supplying these would resolve several outstanding unknowns.
  - Suggested action: Provide file paths and locators for these implementations or include them in the supplied artifacts for review.

### Supported (5)

- **GridServer is a Python backend built on pandapower and streams results to InfluxDB and/or MQTT.**
  - Catalogue: framework_description
  - Evidence: A2 README.md, lines 37-42, 54
  - Assessment: README explicitly states GridServer is Python-based, built on pandapower, and streams to InfluxDB 2 and/or MQTT in real time.
  - Suggested action: Review the cited evidence.
- **Operating modes include automatic, realtime, demo, batch; default step is 15 minutes; global_time and global_step exist.**
  - Catalogue: operating_modes_and_timing
  - Evidence: A2 README.md, lines 52-53, 61-68
  - Assessment: README documents operating modes and time engine variables with a default step of 15 min.
  - Suggested action: Review the cited evidence.
- **The AMiRo network model defines buses, an external grid, a 0.25 MVA transformer, 24 household loads, 24 PV generators and five EV loads, with lines between buses.**
  - Catalogue: amiro_model_contents
  - Evidence: A3 config/grids/amiro_net/amiro_net.py, lines 5-99
  - Assessment: amiro_net.py creates buses (lines 9-18), an ext_grid and transformer (lines 20-22), repeated load and sgen creation patterns that sum to 24 household loads and 24 sgens, plus EV loads (lines 24-35, 62-91).
  - Suggested action: Review the cited evidence.
- **Power-flow calculation uses pandapower's runpp(net) and then export_state(...) is called.**
  - Catalogue: power_flow_execution
  - Evidence: A5 services/gridserver/src/main.py, lines 600-603
  - Assessment: do_power_flow() calls pp.runpp(net) and then export_state(get_global_timestamp(), hh_objects).
  - Suggested action: Review the cited evidence.
- **Project depends on pandapower, paho_mqtt, influxdb-client, plotly, flask, jinja2 and other Python packages.**
  - Catalogue: dependencies
  - Evidence: A6 services/gridserver/requirements.txt, entire file
  - Assessment: requirements.txt lists these packages by name.
  - Suggested action: Review the cited evidence.
