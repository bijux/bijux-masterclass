# Glossary

This glossary keeps the language of Module 03 stable.

| Term | Meaning in Module 03 |
| --- | --- |
| CI contract | The stable target surface and behavior guarantees that automation depends on. |
| convergence | The build reaches a quiet state where a repeated successful run has nothing left to do. |
| deterministic discovery | Rooted, canonical file discovery that stays stable for the same repository state. |
| equivalence set | The declared artifact set used to compare serial and parallel builds. |
| forensic debugging | Debugging that relies on Make-native evidence such as `-n`, `--trace`, and `-p`. |
| hidden input | A build fact that changes output meaning without already appearing as explicit graph evidence. |
| negative test | A deliberate regression case used to prove the selftest can detect a real build-system failure. |
| public target | A target whose meaning is part of the supported interface of the build. |
| semantic stamp | A stamp or manifest that changes only when the modeled semantic input changes. |
| quarantined eval | A bounded, auditable, switchable `eval` surface that does not control the core build. |
