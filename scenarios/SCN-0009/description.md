# SCN-0009 — EV charging and transformer loading in a photovoltaic-rich low-voltage grid

The study evaluates **one** low-voltage grid with three EV charging variants. A transformer connects 24 PV-equipped households to the upstream grid. Fig. 4 depicts four groups of six households, with a 22 kW wallbox in each group and a fast charging station on a separate connection. Grid-Sim-Builder provides the simulation and control interface. The paper discusses mosaik as a related platform. [Paper, §§IV–VI and Fig. 4](https://doi.org/10.1109/SmartGridComm65349.2025.11204608)

## Experiment

The PV input uses irradiation recorded in Bielefeld on 3 August 2019. The authors compare transformer loading with (1) no EV charging, (2) four wallboxes switched on sequentially in response to PV feed-in, and (3) uncontrolled charging from simulated household activity profiles. The fast charger is part of the topology. The reported comparison does not establish its use in the four-wallbox policy. Fig. 6 shows loading curves in percent. The paper does not provide a numerical table of peaks or a reproducible set of switching thresholds. [Paper, §V, Figs. 4–6](https://doi.org/10.1109/SmartGridComm65349.2025.11204608)

## Models, interfaces and timing

The adapted ALPG first generates household profiles. PV synthesis uses system size, orientation, and irradiation. GridServer reads the profiles and runs pandapower. Mosquitto relays MQTT state and control messages, InfluxDB stores time series, Grafana visualizes recorded results, and Node-RED provides a live dashboard and manual controls. The paper assumes ideal communications. MQTT is the integration interface. [Paper, §§III–IV and VII](https://doi.org/10.1109/SmartGridComm65349.2025.11204608)

The published code selects the AMiRo model by default. Its model file contains 24 household loads, 24 PV generators, and five EV loads. This matches the main topology counts in Fig. 4. The code also supports other grids, and a code default does not establish the authors' run settings. The paper describes one-minute **input profiles**. The release README describes a 15-minute default step and separate operating modes. The actual evaluation power-flow stepping and run settings remain unresolved. [Pinned grid model](https://github.com/Carruthion/grid-sim-builder/blob/1a3d59809c93f46d1e5f3adfe941c40d8f49a3ea/config/grids/amiro_net/amiro_net.py) · [Pinned README](https://github.com/Carruthion/grid-sim-builder/blob/1a3d59809c93f46d1e5f3adfe941c40d8f49a3ea/README.md#L49-L70)

## Reuse and reproducibility

The paper provides a [Zenodo code citation](https://doi.org/10.5281/zenodo.15719352) and a [separate household configurator citation](https://doi.org/10.5281/zenodo.15720960). The inspected Grid-Sim-Builder `v0.1` commit contains an **MIT** license at repository root and a compressed demo profile bundle. The exact terms for the Solcast inputs and generated datasets remain unresolved. Pinning the Git commit identifies the application code, whose requirements leave dependencies such as pandapower unpinned. The exact experiment controller, configuration, datasets and software versions remain unresolved. The catalogue was checked statically. [Pinned license](https://github.com/Carruthion/grid-sim-builder/blob/1a3d59809c93f46d1e5f3adfe941c40d8f49a3ea/LICENSE) · [Evidence register](../../evidence/evidence.yaml)
