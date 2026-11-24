# SCN-0004 — Two-subgrid mosaik testbed for distributed SCADA monitoring

Verena Menzel's 2021 master's thesis uses a simulated electricity distribution grid to evaluate process-aware monitoring. The research question is whether a monitor can recognize inconsistencies that require observations from neighbouring subgrids. The testbed adapts the mosaik example to distinguish two monitored subgrids within a larger grid. The catalogue records one shared testbed with four evaluation types. [Thesis, Chapters 3–4](https://www.uni-muenster.de/imperia/md/content/informatik/agremke/masterthesis_menzel_16032021.pdf)

## Components and data flow

The mosaik 2.6.0 simulation combines PV profile replay, residual household loads, PYPOWER grid calculation, remote terminal unit (RTU) simulation, HDF5 recording and web visualization. Household and PV input data are reported at 15-minute intervals. Table 4.1 specifies the component versions. The input interval describes the data and leaves the exact orchestration step unresolved. [Thesis, §4.2.2 and Table 4.1](https://www.uni-muenster.de/imperia/md/content/informatik/agremke/masterthesis_menzel_16032021.pdf)

The adapted grid is recorded as `MOD-0011`. Its lineage links to the mosaik demo catalogued as SCN-0001, while its exact machine-readable case remains unresolved. The PV and household records identify the software and its role. The exact historical inputs and version-specific household model identity remain unresolved. [Thesis, §4.2.2 and Figs. 4.3–4.4](https://www.uni-muenster.de/imperia/md/content/informatik/agremke/masterthesis_menzel_16032021.pdf)

A helper exports simulated readings from the two RTUs to CSV for testing the monitoring prototype. The prototype's monitoring model (`MOD-0012`) evaluates grid consistency using local observations and information from neighbouring subgrids. The CSV export and evaluation are downstream of the co-simulation. The two monitoring scopes capture what the monitor can observe. [Thesis, Chapters 4–5](https://www.uni-muenster.de/imperia/md/content/informatik/agremke/masterthesis_menzel_16032021.pdf)

## Evaluation and limits

The thesis groups tests into normal operation, local checks, combined local and neighbourhood checks, and cases detectable at neighbourhood scope alone. The author reports that neighbourhood checks detected inconsistencies missed by local checks in the studied topology. Simulation timing between measurements also affected some checks. These findings apply to the proof of concept and its particular test data. [Thesis, §§4.1.3 and 6.1](https://www.uni-muenster.de/imperia/md/content/informatik/agremke/masterthesis_menzel_16032021.pdf)

The catalogue captures the architecture, reported versions and functional exchanges. The exact testbed revision, input profiles, configuration files, simulation step and evaluation artifacts remain unresolved. The linked conference paper is supporting literature. Its setup details were kept separate from the thesis extraction. [Evidence register](../../evidence/evidence.yaml) · [Related conference paper](https://doi.org/10.1109/SmartGridComm51999.2021.9632283)
