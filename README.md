# Co-Simulation Scenario Library

An evidence-backed, progressively enrichable catalogue of co-simulation scenarios, initially focusing on mosaik.

## Principles
- Preserve scientific explanations and original sources.
- Separate scenarios from participating models and software packages.
- Document scenario-specific model usage and interactions.
- Never infer missing information as fact; mark it as unknown or unreviewed.
- Keep records traceable and suitable for later enrichment.

## Layout
- `publications/`: publications and source records (one record per source)
- `scenarios/`: scenario descriptions, metadata, participations, interactions
- `models/`: independent model descriptions, once identities are established
- `software/`: software package references
- `evidence/`: supporting claims and locators
- `catalogue/`: overview (can later be generated automatically)

## First record
`SCN-0001` is a **practice/demo record** from the official mosaik demo; it is **not a publication-derived scientific case study**. Some component names are derived from its README; exact instantiated model identities and interactions have **not yet been checked against source code**.

Source: https://gitlab.com/mosaik/examples/mosaik-demo

## Workflow
1. Find a publication or source and record its stable URL/DOI.
2. Determine whether it describes one or more distinct scenarios.
3. Create `SCN-xxxx/description.md`, `scenario.yaml`, `participations.yaml`, `interactions.yaml`.
4. Add citations/evidence for all material extracted claims.
5. Create reusable model records **only** if identities can be established; otherwise retain provisional participations.
6. Review and commit the changes.

## IDs
Use `SCN-0001`, `PUB-0001`, `MOD-0001`, `SW-0001`, `PART-0001`, `INT-0001` etc. Do not reuse IDs for different entities.
