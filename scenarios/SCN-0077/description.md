# Voltage-responsive storage and PV in a low-voltage grid

Demonstrates cyclic data exchange between a power-flow model and storage whose charging responds to local voltage.

The CERBERUS power-flow simulator receives PV and storage power. The storage model uses the grid voltage to decide whether to charge or discharge. The thesis uses this feedback to demonstrate mosaik's cyclic data-flow support. [Thesis, Section 12.4.3 and Appendix J.3](https://oops.uni-oldenburg.de/1768/1/schsim13.pdf)
