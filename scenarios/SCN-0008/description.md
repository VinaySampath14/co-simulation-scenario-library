# SCN-0008 — District heating peak reduction under varying supply temperatures

The paper uses a mosaik co-simulation of a district-heating distribution network in Northern Italy to compare how two peak-shaving strategies respond to lower water supply temperatures. One shared case supports 12 comparison runs: baseline, demand-side management (DSM), and thermal energy storage at each of 120, 110, 100 and 90 °C. [Paper, §§III–IV, pp. 413–415](https://doi.org/10.1109/TSUSC.2024.3449977)

## System and models

The radial delivery network has 202 nodes and 201 edges and supplies 47 buildings. The case includes one thermal plant and a stratified water tank of approximately 26,150 L. It uses typical winter-day conditions. The 120 °C case uses measured thermal-power and mass-flow demand. Lower-temperature demand data come from the study's reference [21]. [Paper, §III, p. 413](https://doi.org/10.1109/TSUSC.2024.3449977)

The plant and thermo-hydraulic network exchange mass flow and temperatures. Building components replay prescribed demand and compute return-water temperature. Weather drives tank losses through outdoor temperature. The paper describes an adapted AixLib tank FMU and a control interface that either schedules storage or advances building demand profiles, depending on the variant. The execution graph reports 60-second steps for most components and 10-second steps for storage. It shows same-step exchanges and time-shifted exchanges used in cyclic data flows. Results are recorded in HDF5. [Paper, §§II-B–C and IV-B, Figs. 3–4 and 8](https://doi.org/10.1109/TSUSC.2024.3449977)

## Reported results and limits

Peak reductions relative to the baseline at each supply temperature, as printed in Table II:

| Supply temperature | Storage | DSM |
| --- | --- | --- |
| 120 °C | 18.0% | 33.3% |
| 110 °C | 17.2% | 33.5% |
| 100 °C | 16.8% | 34.5% |
| 90 °C | 14.9% | 33.4% |

The results text reports the storage endpoints as 18.04% and 14.95%. DSM was less sensitive to lower supply temperatures in this case. The study compares sensitivity to temperature, with results that depend on the selected profiles and control schedules. The authors did not mathematically optimize either schedule. [Paper, §§III–IV, Tables I–II](https://doi.org/10.1109/TSUSC.2024.3449977)

The catalogue records published model designs and functional exchanges. The executable study code, complete network and time-series files, FMU, software versions, exact port mappings, initial conditions, and per-edge timing remain unresolved. [Evidence register](../../evidence/evidence.yaml)
