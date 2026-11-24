# SCN-0005 — mosaik smart-grid demo with ontology export

## Deterministic validation

Catalogue checks: **passed** (34 YAML files, 171 IDs).
Review status: `evidence_checked`. Declared human workflow status: `draft`. Runtime status: `not_run`.

Catalogue packet SHA-256: `6e361d2bd816618e23a768974156493f7781358cb97c274c61555a0ddadd4e18`.

## Review index

- [scenarios/SCN-0005/interactions.yaml](../../scenarios/SCN-0005/interactions.yaml)
- [scenarios/SCN-0005/participations.yaml](../../scenarios/SCN-0005/participations.yaml)
- [scenarios/SCN-0005/scenario.yaml](../../scenarios/SCN-0005/scenario.yaml)
- [scenarios/SCN-0005/description.md](../../scenarios/SCN-0005/description.md)
- [models/MOD-0001.yaml](../../models/MOD-0001.yaml)
- [models/MOD-0002.yaml](../../models/MOD-0002.yaml)
- [models/MOD-0003.yaml](../../models/MOD-0003.yaml)
- [publications/PUB-0001.yaml](../../publications/PUB-0001.yaml)
- [software/software.yaml](../../software/software.yaml)
- [evidence/evidence.yaml](../../evidence/evidence.yaml)

## Original sources and review inputs

- SRC-0018 [User-supplied mosaik-scenario-planning.zip](urn:sha256:e3749b8800868abfd761cffe77515dc7d2193109caec3ce071ed30a4ea3f405f)
- SRC-0001 [mosaik-demo (official repository)](https://gitlab.com/mosaik/examples/mosaik-demo) at `74e2e1b8e53a3bfa1cdbba8897c7e8cd5d23b1e8`
- SRC-0005 [mosaik-householdsim](https://pypi.org/project/mosaik-householdsim/2.2.0/#files) at `2.2.0`
- A1 (SRC-0018) mosaik-scenario-planning-master/README.md — supplied. 04c9aa411a030fa881a32c6e91dedf3d82e0494087516636c6e994dbdebfa20e
- A2 (SRC-0018) mosaik-scenario-planning-master/eval_mosaik_demo/demo_eval.py — supplied. b92b53995d093e0adeac0ec77fb3421ef610c1414386b84d7918d97133e4515f
- A3 (SRC-0018) mosaik-scenario-planning-master/diss_process.py — supplied. 0e3e7d732eb435964a146be29587447dafd92a27acc84f62973e5bf49e584c9c
- A4 (SRC-0018) mosaik-scenario-planning-master/dfg_process.py — supplied. 13b4e55316f79d88e558cc8733ac85bdb4b80a1fc2e831f8d8b768117fb0780b
- A5 (SRC-0018) mosaik-scenario-planning-master/xmind/xmind_im_export_dfg.config — supplied. 5d38192ae850fb2d4fd34b37ae7339bc9eef1a4edc0fb01ab4d4bf32e299103b
- A6 (SRC-0018) mosaik-scenario-planning-master/eval_mosaik_demo/data/demo_lv_grid.json — supplied. e00d453729d58d3b19a8522697aae62386a62539d64b57b1b4f323fff2e686f4
- A7 (SRC-0018) mosaik-scenario-planning-master/pyproject.toml — supplied. 0f25e4823210ef1d9ab6dc7ee250f7f883b2f392e2b1143713e2f05d766a4445
- A8 (SRC-0018) mosaik-scenario-planning-master/uv.lock — supplied. d6ef4fb3f9536fe51efb331accd6176a5a7b143df729894bca76c9f48803235d

## AI-assisted evidence review

Status: **completed**.
Reviewer: `gpt-5-mini`. Source assessment: `consistent`.

The findings require human judgment. The review does not approve the scenario.

- Key modules/ontologies referenced (cosicoca ontology contents, information_model.owl, sparql_handler internals, export_handler internals, validation_handler internals) are not present in supplied artifacts; this prevents verifying semantic matching and validation logic.
- Time-series input files referenced (pv_10kw.csv, profiles.data.gz) are named but their contents were not supplied for inspection (only referenced paths exist); exact sampling/format cannot be verified here.
- The supplied code exports scenario RDF without necessarily executing the simulation (demo_eval may be run with run=False); it is unclear from supplied artifacts whether exported RDF includes runtime traces or only static scenario definitions.

### Needs evidence (1)

- **Exported RDF contains runtime traces (time series) from an executed simulation run.**
  - Catalogue: runtime_traces_in_export
  - Evidence: A2 Ln72–80; A3:Ln86–87
  - Assessment: demo_eval exports scenario RDF (Ln76–80). However, diss_process calls demo_eval.main(..., run=False) (A3:Ln86–87), meaning RDF exported there is produced without running the simulation. There is no supplied evidence that exported RDF includes runtime-recorded time series.
  - Suggested action: Update catalogue to distinguish 'static scenario export' (structure & metadata) from 'runtime trace export' and mark the latter as unverified until a run=True export and its RDF contents are provided.

### Missing metadata (2)

- **The catalogue asserts ontology-driven matching and unit/time-scale checking, but the referenced ontology files and SPARQL handler logic are not supplied for verification.**
  - Catalogue: ontology_and_sparql_internals
  - Evidence: A3 Ln50–61
  - Assessment: diss_process.py calls CosicocaHandler and SPARQLHandler and appends cosicoca.onto to IM (Ln50–56) and later runs components_from_cosicoca and find_suitable_components_for_im (Ln56–75), but the implementations and the actual ontology files are not present in supplied artifacts.
  - Suggested action: Mark catalogue fields that claim detailed SPARQL/unit/dimension validation as 'requires verification' and link to actual ontology/rule sources; or supply sparql_handler.py and the Ontology RDF files so claims can be confirmed.
- **DFG workflow uses the XMind workbook xmind/20201120_Integrated_InformationModel.xmind to build the Information Model.**
  - Catalogue: xmind_workbook_availability
  - Evidence: A5 Ln6–9; A4:Ln103–117
  - Assessment: xmind_im_export_dfg.config points to the XMind workbook (Ln6–9) and dfg_process.py documents reading from it (Ln103–117), but the workbook file itself is not present among supplied artifacts. Thus the exact IM content used by the DFG process cannot be inspected.
  - Suggested action: Record in the catalogue that the XMind workbook is missing and either supply it or mark derived IM outputs as unverifiable.

### Possible hallucination (1)

- **Matched components from CoSiCoCa are automatically added to the mosaik scenario during diss_process.**
  - Catalogue: automatic_component_addition
  - Evidence: A3 Ln70–82
  - Assessment: diss_process obtains chosen_inputs/chosen_outputs via find_suitable_components_for_im (Ln73–75) but only instantiates MosaikScenarioHandler.add_models if choose_option is not False (Ln76–82). In the provided script choose_option is set to False (Ln70–71), so automatic addition is skipped. The catalogue should not assert automatic instantiation here without noting the conditional.
  - Suggested action: Correct catalogue to state that component addition is conditional; note that in the supplied orchestration the add_models path is not executed (choose_option=False).

### Human question (1)

- **Is the exported scenario RDF intended to include runtime series (if so, which export step), or only the structural scenario?**
  - Catalogue: No existing field
  - Evidence: Unresolved
  - Assessment: Code paths show both possibilities: demo_eval can run simulation (run=True) and then exports, while diss_process explicitly calls demo_eval with run=False before validation (A2:Ln86–87; A3:Ln86–87). The supplied artifacts do not clarify the intended semantics of the exported RDF in each workflow.
  - Suggested action: Catalogue should record this question and request clarification or an example exported RDF showing runtime traces (if intended).

### Supported (3)

- **The repository implements ontology-based scenario planning: IM -> CoSiCoCa -> mosaik scenario export -> validation (dissertation workflow).**
  - Catalogue: scenario_purpose
  - Evidence: A1 Ln61–76
  - Assessment: README explicitly describes the dissertation workflow chaining Information Model, CoSiCoCa, mosaik scenario export and validation.
  - Suggested action: Review the cited evidence.
- **Demo uses PyPower (grid), HouseholdSim (households), CSV adapter (PV time series) and mosaik-hdf5 (database recorder).**
  - Catalogue: demo_simulators_and_roles
  - Evidence: A2 Ln19–40; Ln100–127
  - Assessment: SIM_CONFIG lists adapters and create_scenario starts PyPower, HouseholdSim, CSV and a DB recorder; code instantiates grid, houses, PVs and HDF5 recorder.
  - Suggested action: Review the cited evidence.
- **Houses connect to grid nodes mapping 'P_out' -> 'P'; PVs connect to node 'P'; node/branch variables (P,Q,Vl,Vm,Va,P_from,Q_from,P_to,Q_to) are written to HDF5.**
  - Catalogue: connections_and_monitored_attributes
  - Evidence: A2 Ln121–136; Ln205–211
  - Assessment: connect_buildings_to_grid connects house P_out to bus P (Ln205–211); connect_randomly connects PVs to node 'P' (Ln121–123). Many-to-one connections to HDF5 list the attributes recorded (Ln125–136).
  - Suggested action: Review the cited evidence.
