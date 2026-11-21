# SCN-0001 — mosaik Smart Grid Demo

**Record type:** Software demonstration / practice entry (not a peer-reviewed publication-based study).

## Scientific/technical purpose
The official mosaik demonstration illustrates the coupling of a simplified electrical grid with household electricity demand and photovoltaic (PV) generation through mosaik. It is designed to demonstrate how components from the mosaik ecosystem can participate in a smart-grid co-simulation.

## System investigated
A simplified electricity distribution grid with household loads and PV generation. The official live-demo description refers to scenarios representing different months and levels of PV active power.

## Components reported in official documentation
- PYPOWER-based grid calculation, integrated through `mosaik-pypower`.
- PV time-series data, integrated through `mosaik-csv`.
- Household demand data, represented using `mosaik-householdsim`.
- `mosaik-web` for visualization.
- `mosaik-hdf5` for storing results.

These are *reported software components*, not yet individually identified underlying mathematical model definitions.

## Interactions
Not yet verified from `demo.py`. Do not infer exact attributes, directions, or time steps from component descriptions alone.

## Outcomes
The public demo illustrates a working co-simulation; this entry does not claim experimental scientific results.

## Open questions for later investigation
- Exact model entities started in `demo.py`?
- Exact data connections and exchanged attributes?
- Which grid network and PV/household input data are used?
- What are the configured simulation parameters and software versions?

## Sources
1. Official demo source: https://gitlab.com/mosaik/examples/mosaik-demo
2. Live-demo explanation: https://mosaik.offis.de/live-demo/
3. Documentation: https://mosaik.offis.de/docs/

**Review status:** Initial collection from repository README and official descriptions; source-code-level review pending.
