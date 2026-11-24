# SCN-0003 — Distribution-grid flexibility control in a cyber-physical laboratory

Hacker et al. (2021) tested whether the same energy-management logic could control simulated or physical flexibility resources. The catalogue records the four-household laboratory setup as one scenario with a baseline and three control variants. The paper also describes a pure mosaik simulation mode in which pandapower replaces the physical grid. The authors used the Docker deployment for the reported experiments. [CIRED paper, §§2–4](https://doi.org/10.1049/icp.2021.1777)

## Components and exchanges

- **Virtual Edge Device (VED).** Interfaces update a shared state store before the control logic runs. The interfaces then send the resulting setpoints to equipment or simulated devices. In pure simulation, the profile reader supplies domestic load and solar generation to the household VEDs, which send active and reactive power to a balanced, single-phase power-flow calculation at each step.
- **Physical laboratory.** Two low-voltage feeders share a 630 kVA transformer and supply four household emulations. Load banks represent domestic and EV charging demand, and controllable DC supplies drive PV inverters. The household coupling points and the transformer low-voltage side have measurement points. Household 2 can use a 15 kW, 15 kWh battery.
- **Time and deployment.** The laboratory profiles use 15-minute simulated intervals. The authors report four setpoints per wall-clock minute and a 60× acceleration factor. Containernet is described as an available network-emulation component. Its use in the three reported experiments is unresolved.

## Control variants and reported results

| Variant | What it does |
| --- | --- |
| Baseline | Runs with management inactive. Figure 4 uses household 2 without a connected battery as its reference. |
| Direct battery dispatch | Uses current household power conditions to control household 2's battery for self-consumption. |
| Forecast battery dispatch | Uses predicted load and generation to optimize household 2's battery dispatch over one day. |
| Transformer congestion control | Uses transformer measurements to signal households 1 and 2 to enter a restricted mode. Their VEDs reduce emulated EV charging, with a 5 kW household limit in restricted mode. The transformer threshold is 35 kW. |

Both battery strategies reduced household 2's exchange with the grid during much of the reported day, while the battery could not cover the EV charging peaks. The congestion controller reduced transformer loading relative to the 58 kW baseline peak, though limited controllable load prevented it from holding every peak below the 35 kW target. These results characterize the laboratory tests. The paper focuses on energy-management timescales. [CIRED paper, §§4–5 and Figs. 4–5](https://doi.org/10.1049/icp.2021.1777)

## Reproducibility

The four new model records capture the published VED architecture and controller designs. The exact profile and forecast datasets, controller implementations and optimizer settings, electrical feeder parameters, interface bindings, and software versions remain unresolved. The laboratory battery ratings establish equipment capabilities. The paper describes a separate simulated battery interface that updates state of charge using efficiency, with its exact equations and parameters unresolved. [Evidence register](../../evidence/evidence.yaml)
