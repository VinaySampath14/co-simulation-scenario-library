# Model registry

Each `MOD-xxxx.yaml` record identifies a model by its definition and supporting evidence. A model can be a network case, a prescribed time series, or a behavioral implementation. Scenario-specific parameters and entity counts belong in the participation records. When only a reported model name is available, keep it with the participation and leave the model ID unresolved.

A prescribed time series supplies values at given times. A physical or mathematical generation model describes how those values are produced. For example, [MOD-0002](MOD-0002.yaml) identifies the PV input series used in SCN-0001. Its values are replayed by the CSV adapter, and their production method remains unknown.
