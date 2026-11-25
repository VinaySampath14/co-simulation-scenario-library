# Vertical scaling of a building multi-energy co-simulation

Benchmarks how the runtime of a mosaik-based building energy co-simulation changes as more model instances are added.

The COESI scenario includes building, heat pump, PV, battery, household behaviour, weather and smart meter models. Profiling identifies PV computation as the main bottleneck in the tested setup. The authors compare multiprocessing and Ray-based approaches for that simulator. [PDF pp. 4–6, Sections III?IV and Figures 2–3](https://doi.org/10.1109/COMPSAC65507.2025.00286)
