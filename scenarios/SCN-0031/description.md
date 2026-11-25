# FMI 3 communication delays in distribution-grid tap control

Demonstrates hybrid co-simulation with mosaik 3 by combining grid power flow, a tap controller and an event-driven communications model.

The grid is represented in pandapower and receives time-series loads. Voltage measurements travel through a communication queue to a Python tap changer controller. The communication simulator uses FMI 3.0 and has deterministic and probabilistic variants. The remaining simulators are coupled using FMI 2.0. [PDF p. 6, printed p. 40, Figure 3 and accompanying text](https://doi.org/10.1007/978-3-031-99451-7_4)
