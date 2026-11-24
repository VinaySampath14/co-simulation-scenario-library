# SCN-0008 — District heating peak reduction under varying supply temperatures

## Deterministic validation

Catalogue checks: **passed** (56 YAML files, 243 IDs).
Review status: `evidence_checked`. Declared human workflow status: `draft`. Runtime status: `not_run`.

Catalogue packet SHA-256: `375362f560bb327ff44fc2a717bafc32c4be4b6c122d72e824981ad91ee9fbe2`.

## Review index

- [scenarios/SCN-0008/interactions.yaml](../../scenarios/SCN-0008/interactions.yaml)
- [scenarios/SCN-0008/participations.yaml](../../scenarios/SCN-0008/participations.yaml)
- [scenarios/SCN-0008/scenario.yaml](../../scenarios/SCN-0008/scenario.yaml)
- [scenarios/SCN-0008/description.md](../../scenarios/SCN-0008/description.md)
- [models/MOD-0018.yaml](../../models/MOD-0018.yaml)
- [models/MOD-0019.yaml](../../models/MOD-0019.yaml)
- [models/MOD-0020.yaml](../../models/MOD-0020.yaml)
- [models/MOD-0021.yaml](../../models/MOD-0021.yaml)
- [models/MOD-0022.yaml](../../models/MOD-0022.yaml)
- [models/MOD-0023.yaml](../../models/MOD-0023.yaml)
- [publications/PUB-0007.yaml](../../publications/PUB-0007.yaml)
- [software/software.yaml](../../software/software.yaml)
- [evidence/evidence.yaml](../../evidence/evidence.yaml)

## Original sources and review inputs

- Primary publication: [A Modular Co-Simulation Platform for Comparing Flexibility Solutions in District Heating Under Variable Operating Conditions](https://doi.org/10.1109/TSUSC.2024.3449977)
- SRC-0020 [Mazzarino et al. (2025), district heating flexibility co-simulation](https://doi.org/10.1109/TSUSC.2024.3449977) at `version_of_record`
- A1 (SRC-0020) A_Modular_Co-Simulation_Platform_for_Comparing_Flexibility_Solutions_in_District_Heating_Under_Variable_Operating_Conditions.pdf — supplied. cc34a4d05aec405babf53b5edabf5786ba41dfecfdf35ddb69ee595758984c56

## AI-assisted evidence review

Status: **completed**.
Reviewer: `gpt-5-mini`. Source assessment: `consistent`.

The findings require human judgment. The review does not approve the scenario.

- No executable code, FMU file, or simulation input dataset (time series / network files) supplied in the artifact — prevents runtime verification.
- Thermal storage FMU export/validation details (tests comparing original Modelica model vs FMU) are not provided.
- Control strategies are described as 'semi-optimized' or rule-based; no optimization algorithm or full pseudo-code is present.
- Results derive from a single case study topology and specific DSM/storage schedules; generalizability to other networks is not demonstrated.
- Time‑shifted exchange is described as an approximation; numerical/temporal error bounds or initialization procedure details are not provided.

### Needs evidence (2)

- **Modified AixLib Modelica tank exported to FMU — equivalence to original Modelica model and numerical validation are assumed but not shown.**
  - Catalogue: fmu_validation_and_equivalence
  - Evidence: A1 §II-B, p. 411 (statement: 'modifications only regard the interfaces ... without affecting the validity of the underlying physical model from AixLib')
  - Assessment: Authors state interface-only modifications but provide no validation data comparing FMU vs original Modelica model.
  - Suggested action: Record as 'validation tests absent'; catalogue should flag FMU artifact as 'not provided / validation not reported' and require addition of FMU verification artifacts.
- **Time‑shifted messaging is used to resolve cyclic data flows but numerical impact/accuracy implications are not quantified.**
  - Catalogue: numerical_error_and_time_shift_impact
  - Evidence: A1 §IV-B, pp. 415–416; Fig. 8 (p. 416)
  - Assessment: Paper acknowledges approximation and initialization need but does not quantify errors introduced by time‑shifts or provide tests.
  - Suggested action: Recommend adding sensitivity/verification tests quantifying error from time-shifted exchanges and differing timestep resolutions.

### Missing metadata (3)

- **No code URL, software versions, FMU files, or raw simulation inputs (time series, network topology files) are provided in the paper.**
  - Catalogue: code_and_data_availability
  - Evidence: A1 No explicit locator — absence across paper (see Sections II–IV and Conclusion where modularity and plug&play are claimed but no repository is given).
  - Assessment: Paper does not supply links or attachments for reproducibility (authors note modularity and plug&play but do not publish artifacts).
  - Suggested action: Catalogue should mark code_url and FMU artifacts as 'missing' and request deposit of FMUs, Python APIs, MOSAIK scenario scripts, and input datasets.
- **Specific software versions (MOSAIK version, Python packages, Modelica/AixLib version, FMU export toolchain) are not listed.**
  - Catalogue: software_versions_and_dependencies
  - Evidence: A1 No explicit locator — absence across methodology and implementation descriptions (see §II-B and Conclusion).
  - Assessment: Paper names tools (MOSAIK, AixLib) but omits versioning which is important for reproducibility.
  - Suggested action: Catalogue should include fields for software versions; request authors to provide exact versions and FMU export settings.
- **Exact initial conditions, per-pipe diameters/lengths, insulation properties, node elevations, and detailed network parameters used in the synthetic or real network are not fully enumerated.**
  - Catalogue: initial_conditions_and_network_parameters
  - Evidence: A1 §II-A and §III, pp. 410–414 (discussion of synthetic grid creation and topology) — detailed per-edge parameters are not listed.
  - Assessment: Paper describes general dimensioning principles and archetype composition but does not publish per-edge parameter tables necessary for exact replication.
  - Suggested action: Catalogue should mark network parameter set as 'not provided' and request a network data file or table.

### Possible hallucination (1)

- **Paper does not provide a detailed thermodynamic explanation for why storage effectiveness declines with lower supply temperatures; any such explanation in the catalogue would be an inference rather than supported by explicit text.**
  - Catalogue: thermodynamic_explanation_of_storage_degradation
  - Evidence: A1 §IV, pp. 414–415 (results and brief discussion)
  - Assessment: The paper reports the empirical trend but does not provide a detailed mechanistic thermodynamic analysis; catalogue should avoid asserting causes beyond authors' statements.
  - Suggested action: Avoid adding causal explanations in catalogue; if necessary, label as 'inference' and request authors for mechanistic analysis or sensitivity tests.

### Supported (9)

- **Framework purpose: modular Plug&Play MOSAIK co-simulation platform to compare TES and DSM flexibility strategies in district heating under varying supply temperatures.**
  - Catalogue: purpose
  - Evidence: A1 Abstract and Introduction, pp. 408–410
  - Assessment: Paper explicitly states the framework purpose in Abstract and Introduction.
  - Suggested action: Review the cited evidence.
- **Co-simulation engine: MOSAIK orchestrator and MOSAIK Python APIs manage synchronization, instantiation and data-exchange.**
  - Catalogue: co-simulation_engine
  - Evidence: A1 §II-B, pp. 410–412; Fig. 1 (p. 410)
  - Assessment: Section II-B and Fig. 1 describe MOSAIK use and roles.
  - Suggested action: Review the cited evidence.
- **Operational Layer includes: Thermal power plant (Python), DH grid (1-D quasi-steady Python model; Eqs. 1–3), Thermal storage (AixLib Modelica-derived FMU exposing Charging/Discharging temp & mass-flow, External temp, Top/Bottom temps), Control strategy (Python), Weather and Building as time-series readers.**
  - Catalogue: models_and_interfaces
  - Evidence: A1 §II-B, pp. 410–412; Fig. 3 (p. 411); Equations (1)–(3) (p. 411–412)
  - Assessment: Paper lists models, implementation types and TES FMU I/O in Section II-B and Fig. 3; DH equations are provided as (1)–(3).
  - Suggested action: Review the cited evidence.
- **Directional exchanges and sequence: preliminary Control→(Storage schedule or Building anticipatory profile) and numbered calculation flows as in Fig. 4 (Building → plant+grid; Weather→storage; Storage→plant+grid when charging/discharging; Plant→grid; Grid→Building+Storage; Building→Grid return; Grid→Plant).**
  - Catalogue: co-simulation_workflow
  - Evidence: A1 §II-C, p. 412; Fig. 4 (p. 412)
  - Assessment: Fig. 4 and Section II‑C explicitly enumerate and describe the numbered message flows.
  - Suggested action: Review the cited evidence.
- **Most simulators use 60 s time step; Thermal storage FMU stepped every 10 s; framework uses time‑shifted messaging to resolve cyclic data flows.**
  - Catalogue: time_resolution
  - Evidence: A1 §IV-B, p. 415–416; Fig. 8 (p. 416)
  - Assessment: Section IV-B and Fig. 8 show execution graph and state that storage is stepped at 10 s while others at 60 s; time-shifted exchange is discussed.
  - Suggested action: Review the cited evidence.
- **Case study: radial delivery sub-network (202 nodes / 201 edges), 47 buildings, 1 thermal storage (~26,150 L), 1 thermal power plant; simulations run for supply temperatures 120, 110, 100, 90 °C.**
  - Catalogue: experimental_setup
  - Evidence: A1 §III, pp. 413–414; Fig. 5 (p. 413); §III and Table I (p. 414)
  - Assessment: Section III and figures/tables describe the topology, counts, storage capacity, and supply temperature scenarios.
  - Suggested action: Review the cited evidence.
- **Control strategies implemented: (i) TES schedule — charge 03:00–05:20 at ~3.094 kg/s and discharge ~06:00–07:00 with variable flow proportional to peak slope; (ii) DSM — advance selected building load profiles (majority by 30 minutes; Table I shows per-building advance distribution).**
  - Catalogue: control_strategy_descriptions
  - Evidence: A1 §III and §IV, pp. 413–414; Table I (p. 414)
  - Assessment: Paper gives charge/discharge schedule and DSM shift configuration; authors state schedules are not mathematically optimized.
  - Suggested action: Review the cited evidence.
- **Reported peak reduction: Storage strategy declines with lower inlet temperature (example values: 18.04% at 120 °C → 14.95% at 90 °C). DSM produces roughly constant reduction (~33–34%) across supply temperatures; maximum DSM variation ~1.22 percentage points.**
  - Catalogue: results_peak_reduction
  - Evidence: A1 §IV, pp. 414–415; Table II and Fig. 6 (p. 414)
  - Assessment: Section IV discusses and Table II (with Fig. 6) provides the numeric/visual results and the quoted percentages.
  - Suggested action: Review the cited evidence.
- **Authors acknowledge that direct performance comparison with monolithic platforms (e.g., Modelica) is not straightforward and that optimal scheduling is out of scope.**
  - Catalogue: authors_caveats
  - Evidence: A1 Conclusion, p. 416
  - Assessment: Paper explicitly states these limitations in the Conclusion.
  - Suggested action: Review the cited evidence.
