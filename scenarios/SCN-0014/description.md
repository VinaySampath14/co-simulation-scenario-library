# Carbon-emissions effects of solar PV in a wind-enabled benchmark grid

The authors demonstrate a carbon-emissions simulator in a mosaik co-simulation of a CIGRE benchmark electricity network, implemented in pandapower using SimBench. The setup uses standalone solar PV and wind simulators and includes local loads, conventional diesel generation and exchange with an external grid. The emissions simulator uses emission factors to estimate the carbon footprint, including time-varying emissions from imported electricity. The showcase uses Lower Saxony as its regional setting. [Paper, showcase section and Figure 2](https://doi.org/10.5281/zenodo.13984401)

The authors compare two configurations of the same showcase over one day, with and without PV. They report that midday solar generation displaces conventional supply and lowers estimated emissions in the PV configuration. [Paper, showcase section and Figure 3](https://doi.org/10.5281/zenodo.13984401)

The paper links a public simulator repository and points to examples in its demo folder. The exact revision used for the published showcase remains unverified. [Repository](https://gitlab.com/mosaik/components/energy/mosaikemissions)
