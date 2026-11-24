# SCN-0002 — Urban multi-energy co-simulation scalability benchmark

Barbierato et al. (2022) used a simplified urban energy system to compare the scalability of mosaik, HELICS and an orchestration implementation built with the AIOMAS agent library. This catalogue records one scenario because the seven test configurations share a physical workload and vary its deployment and instance count. The benchmark studies orchestration performance as the workload grows. [Paper, setup and Fig. 6](https://link.springer.com/content/pdf/10.1186/s42162-022-00231-6.pdf#page=13)

## Components and exchanges

| Component | Role in the benchmark | Reported resolution |
| --- | --- | --- |
| Weather reader | Reads an EPW file and supplies temperature, solar irradiance and humidity to the PV and building simulators. | 15 min |
| PV model (`MOD-0004`) | Estimates generation from weather and panel area, with NOCT or Mattei cell-temperature estimation depending on availability of wind input. Sends generated power to the grid. | 15 min |
| Building and heat-pump model (`MOD-0005`) | Uses a resistance-capacitance representation of the building envelope and tracks indoor temperature between steps. Sends current heat-pump electrical demand to the grid. | 1 h |
| Distribution-network model basis (`MOD-0006`) | Uses pandapower to solve power flow with the building demand and PV generation. The paper describes an event trigger on receipt of both inputs. | 1 h |

The paper describes the PV service's energy estimate and identifies power as the signal sent to the grid. Exact exchange units, attribute names, wind availability in the benchmark, and the handling of 15-minute PV values at the hourly grid boundary remain unknown. The benchmark identifies the grid's published model basis. The exact network file and allocation of PV and building instances to buses remain unresolved. [Component descriptions](https://link.springer.com/content/pdf/10.1186/s42162-022-00231-6.pdf#page=15) · [Grid scheduling](https://link.springer.com/content/pdf/10.1186/s42162-022-00231-6.pdf#page=16)

## Benchmark configurations and results

The authors simulated seven winter days. Weather and power flow each have one instance, and the PV and building populations grow together from 1 to 100, 10,000, 100,000 and 1,000,000 instances per scaled component, with the tested mosaik variants stopping at 10,000. Four OpenStack worker nodes host the components, with a separate master node for configurations that use a central orchestrator. The seven variants are classic mosaik and HELICS, their respective multiprocess setups, standalone AIOMAS orchestration, and mosaik or HELICS with encapsulated AIOMAS simulators. [Configuration and deployment](https://link.springer.com/content/pdf/10.1186/s42162-022-00231-6.pdf#page=16) · [Tables 1–2](https://link.springer.com/content/pdf/10.1186/s42162-022-00231-6.pdf#page=17)

The study measures setup time, the slowest simulator's mean wall-clock step duration and total execution time. Multiprocess HELICS performed best at the largest tested scale. The reported 10,000-instance limit applies to the study's mosaik configuration and message sizes. The authors identify the selected workload as a limitation on generalizing the timing results. [Metric definitions](https://link.springer.com/content/pdf/10.1186/s42162-022-00231-6.pdf#page=12) · [Reported results and conclusion](https://link.springer.com/content/pdf/10.1186/s42162-022-00231-6.pdf#page=23)

## Reproducibility

The record is based on the paper and its cited model sources. The paper gives the weather file format and the run season, but the specific EPW file, dates, framework versions, exact exchanged attributes and runnable benchmark implementation remain unresolved. The paper's availability section provides no artifact link, and the review did not identify a public benchmark repository. See the [evidence register](../../evidence/evidence.yaml) for individual claim locators. [Availability statement](https://link.springer.com/content/pdf/10.1186/s42162-022-00231-6.pdf#page=24)
