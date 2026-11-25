# HVAC controller benchmarking with the UMAR building digital twin

The authors benchmark building automation and control using BAC-Bench, a calibrated digital twin of Empa’s Urban Mining and Recycling (UMAR) unit. They compare a rule-based HVAC controller, an energy-minimizing predictive HVAC controller, and an emissions-minimizing predictive controller with a broader set of assets. The comparisons use the same boundary conditions and assess energy use and thermal comfort at room level. [Paper, Sections 2 and 3.2 and Table 2](https://www.energy-proceedings.org/wp-content/uploads/cen2022/1651648655.pdf)

Figure 3 describes how mosaik synchronizes the physical unit, the digital twin, the controller, and other components. The broader control configuration includes domestic hot water, an electric vehicle, solar PV, and battery storage. The paper reports a field experiment and digital-twin comparisons, and describes online deployment of BAC-Bench as still undergoing testing and validation. [Paper, Section 2.2 and Figure 3](https://www.energy-proceedings.org/wp-content/uploads/cen2022/1651648655.pdf)

The public nestli benchmark repository cites the paper and lists AGPL-3.0 for the repository software. The exact revision and coverage of the paper’s mosaik integration in the public repository remain unverified. [nestli repository](https://github.com/uesl-empa/nestli)
