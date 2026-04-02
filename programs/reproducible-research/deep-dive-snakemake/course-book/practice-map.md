<a id="top"></a>

# Practice Map

This page collects the main practice surfaces for the whole course in one place.

Use it when you want to know what to build, what to run, and what the run is supposed to
prove before you enter the capstone.

---

## Module Practice Surfaces

| Module | Primary practice surface | Main proof loop | Best capstone follow-up |
| --- | --- | --- | --- |
| 01 | tiny file-contract workflow | `snakemake -n`, then one concrete target | inspect stable output patterns only after the local contract is predictable |
| 02 | dynamic-discovery lab with checkpoints | `snakemake -n`, `snakemake --summary` | compare discovered outputs with the capstone checkpoint story |
| 03 | profile-driven workflow lab | `snakemake --profile profiles/local -n`, then `--profile profiles/ci -n` | inspect verification and operating-policy targets |
| 04 | modular repository sketch | `snakemake --list-rules`, `snakemake -n` | compare local module boundaries with `FILE_API.md` |
| 05 | rule-and-script split lab | `snakemake -n`, then one end-to-end run with recorded environment evidence | inspect scripts, packages, and environment boundaries together |
| 06 | versioned publish lab | `snakemake --summary`, then `snakemake publish/v1/manifest.json` | inspect `publish/v1/` and manifest structure deliberately |
| 07 | architecture review lab | `snakemake --list-rules`, `snakemake --summary` | read `Snakefile`, `workflow/rules/`, and `FILE_API.md` in sequence |
| 08 | multi-profile operating lab | compare local, CI, and scheduler dry-runs | inspect `profiles/` and the Makefile policy targets together |
| 09 | incident review lab | `snakemake -n -p`, `snakemake --list-changes input code params` | compare logs, benchmarks, and verification surfaces |
| 10 | written workflow review | review rubric plus evidence commands | use the capstone as the specimen for governance and migration judgment |

[Back to top](#top)

---

## Three Reusable Proof Loops

### Contract loop

Use when you are checking whether the rule graph and outputs are explicit enough.

```bash
snakemake -n
snakemake --summary
```

### Operating loop

Use when you are checking whether policy changes execution context without changing
meaning.

```bash
snakemake --profile profiles/local -n
snakemake --profile profiles/ci -n
```

### Incident loop

Use when you are investigating slow, noisy, or surprising behavior.

```bash
snakemake -n -p
snakemake --summary
snakemake --list-changes input code params
```

[Back to top](#top)

---

## Best Study Habit

For each module:

1. build the smallest local example first
2. write down what the proof command is supposed to demonstrate
3. run the proof command and explain the result in words
4. enter the capstone only after the local result is legible

That order keeps the course centered on comprehension instead of repository tourism.

[Back to top](#top)
