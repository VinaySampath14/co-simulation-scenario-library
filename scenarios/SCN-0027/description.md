# FMI-based building energy co-simulation with PV and a heat pump

Demonstrates the integration of a building simulation with external models in mosaik using FMI. The example examines combined household demand, heat pump use and PV production.

The EnergyPlus building model exchanges inputs and outputs with Python models of weather, household behaviour and photovoltaic production. A heat pump supplies building heat, and the study tracks household and heat-pump electrical consumption alongside PV generation. A virtual smart meter collects and reports those electrical readings. [PDF pages 4–6, component descriptions and results](https://doi.org/10.1109/EEEIC/ICPSEurope49358.2020.9160641)
