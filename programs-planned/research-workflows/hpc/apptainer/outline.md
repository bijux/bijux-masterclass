# Apptainer Deep Dive

## Module 01: First Principles — The HPC Container Contract

### 01. Mental Model: SIF Immutability, OCI Inputs, and What Apptainer Optimizes For

* SIF (single immutable artifact) vs OCI layers (build source vs run artifact)
* UID/GID identity: you are the same user inside/outside (no silent privilege escalation)
* Isolation *by integration*: namespaces used to run safely on shared HPC, not to mimic VMs

### 02. Security Models Up Front: setuid vs User Namespaces (and Why You Care)

* setuid install vs non-setuid (user-namespace) install: operational consequences
* What features depend on which model (and why clusters often restrict them)
* Practical threat model: mounts, host FS exposure, secrets, and least-privilege defaults

### 03. Filesystem Contract: Binds, Path Discipline, and Scratch-as-a-First-Class Concept

* Default binds (home/cwd/system) and controlling them (`--no-home`, `--pwd`, etc.)
* Explicit binds: `--bind`, precedence, read-only binds, stable path contracts for pipelines
* Data locality: binding node-local scratch for heavy I/O (stage-in/stage-out mindset)

### 04. Writable Views: Overlay Deep Dive + `--writable-tmpfs`

* OverlayFS as the mechanism for “write on top of immutable SIF”
* Persistent overlays: directory overlays vs file-backed ext3 overlays (`--overlay`)
* Ephemeral writes: `--writable-tmpfs` for fast, disposable scratch layers
* Choosing overlays for portability vs performance vs governance constraints

### 05. Runtime Surface: `run`/`exec`/`shell`, Environment Control, and Specialized Mounts

* Entrypoints: `%runscript`, argument passing, runtime expectations
* Environment discipline: `--cleanenv`, `--env`, `APPTAINERENV_*`, library-path control
* GPUs/MPI/network are mostly host-coupled; **FUSE mounts** via `--fusemount` for special FS needs

## Module 02: Building Images — Definition Files, Fakeroot, and Supply-Chain Discipline

### 01. Definition Files as a Build Contract

* `%setup`, `%files`, `%post`, `%environment`, `%runscript`, `%labels`
* Keep recipes minimal and deterministic; separate build-time vs runtime deps
* Bootstraps: `Bootstrap: docker` / library / localimage; pin by digest to prevent drift

### 02. Fakeroot: Root-Like Inside, Not Root on the Host

* `--fakeroot` model: user namespaces to perform privileged-like installation steps
* Prereqs: subuid/subgid mappings; cluster realities and common limitations
* Practical use: package installs, permissions fixes, controlled cleanup, reproducible ownership

### 03. Python/Conda Toolchains (HPC-Realistic Patterns)

* Conda/mamba inside containers: reproducibility pitfalls and mitigation (lockfiles, pinned channels)
* System libs vs conda libs; glibc and binary compatibility constraints
* Performance hygiene: reduce solver churn, freeze environments, keep images lean

### 04. MPI Compatibility Builds (The Real HPC Constraint)

* Host MPI vs container MPI: ABI compatibility and “what must match”
* Binding host libs and interconnect specifics (RDMA/Infiniband realities)
* Testing strategy: login node vs compute node vs multi-node validation

### 05. Trust: Signing, Verification, and Execution Policy

* Signing SIFs; verification in shared environments
* Controlled distribution: internal registries/artifact stores
* Policy enforcement (e.g., allow-listing signed images) as a governance primitive

## Module 03: Production Operations — Performance, Debugging, Governance

### 01. SLURM Integration Patterns (Single-Node and Multi-Node)

* `srun`/`sbatch` execution, cgroups interaction, CPU/mem binding expectations
* MPI launch patterns: task-per-rank, environment propagation, failure handling
* Job hygiene: logs, exit codes, and reproducible job wrappers

### 02. Data Locality and I/O Performance (Where Containers Fail in Practice)

* Shared FS bottlenecks: metadata storms, small-file traps, hot directories
* Explicit stage-in/stage-out to node-local scratch; bind strategy for high-throughput I/O
* Overlay-on-fast-local storage as a write-performance lever when allowed

### 03. Debugging and Diagnostics (Minimal Repros, Not Folklore)

* Common failures: missing libs, bad binds, permissions, UID/GID mismatches, CUDA driver mismatches
* Tools: `apptainer inspect`, interactive `exec`, `--debug`, controlled environment toggles
* Attribution: CPU/memory/I/O profiling at the host process level (what is actually slow)

### 04. Security in Multi-User Reality: Secrets, Mounts, and Safe Defaults

* Handling tokens/credentials/SSH keys safely (avoid baking secrets into images)
* Reducing host exposure: tighten binds, clean env, explicit working dirs
* Practical “safe baseline” run flags for shared clusters

### 05. Governance: Image Lifecycle, CI/CD, Compatibility Guarantees

* CI pipeline: build → test → sign → publish → deprecate
* Compatibility matrix management: CUDA/driver, glibc, kernel, MPI vendor/version
* Versioning policy: immutable artifacts, reproducible research, controlled upgrades
