# Fault Injector

A deliberately small dependency emulator for Course 4 game days. The control endpoint is disabled unless `FAULT_CONTROL_ENABLED=true`; production code must never enable it. Profiles are `healthy`, `slow`, `fail`, `flaky`, and `drop`.
