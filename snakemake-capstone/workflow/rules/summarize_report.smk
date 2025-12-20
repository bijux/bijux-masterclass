# workflow/rules/summarize_report.smk
from __future__ import annotations

RESULTS = config["results_dir"]
PUBLISH = config["publish_dir"]
LOGS = config["logs_dir"]
BENCH = config["benchmarks_dir"]
V = config["params"]["publish"]["version"]

# -----------------------------
# Summarize per-sample results
# -----------------------------
rule summarize:
    input:
        qc_raw_json=lambda wc: expand(f"{RESULTS}/{{sample}}/qc_raw.json", sample=get_samples()),
        trim_json=lambda wc: expand(f"{RESULTS}/{{sample}}/trim.json", sample=get_samples()),
        qc_trimmed_json=lambda wc: expand(f"{RESULTS}/{{sample}}/qc_trimmed.json", sample=get_samples()),
        dedup_json=lambda wc: expand(f"{RESULTS}/{{sample}}/dedup.json", sample=get_samples()),
        kmer_json=lambda wc: expand(f"{RESULTS}/{{sample}}/kmer.json", sample=get_samples()),
        screen_json=lambda wc: expand(f"{RESULTS}/{{sample}}/screen.json", sample=get_samples()),
    output:
        json=f"{PUBLISH}/{V}/summary.json",
        tsv=f"{PUBLISH}/{V}/summary.tsv",
    log:
        f"{LOGS}/summarize.log"
    benchmark:
        f"{BENCH}/summarize.txt"
    conda:
        config["_env_python"]
    resources:
        mem_mb=1000
    params:
        # avoid "benchmark" usage inside shell; mkdir BENCH via params
        benchdir=BENCH,
        pythonpath=PYTHONPATH,
        # build CLI arg lists deterministically from the same sample order
        unit_args=lambda wc: " ".join(f"--unit {s}" for s in get_samples()),
        qc_raw_args=lambda wc: " ".join(f"--qc-raw {RESULTS}/{s}/qc_raw.json" for s in get_samples()),
        trim_args=lambda wc: " ".join(f"--trim-json {RESULTS}/{s}/trim.json" for s in get_samples()),
        qc_trimmed_args=lambda wc: " ".join(f"--qc-trimmed {RESULTS}/{s}/qc_trimmed.json" for s in get_samples()),
        dedup_args=lambda wc: " ".join(f"--dedup-json {RESULTS}/{s}/dedup.json" for s in get_samples()),
        kmer_args=lambda wc: " ".join(f"--kmer-json {RESULTS}/{s}/kmer.json" for s in get_samples()),
        screen_args=lambda wc: " ".join(f"--screen-json {RESULTS}/{s}/screen.json" for s in get_samples()),
    shell:
        r"""
        set -euo pipefail

        mkdir -p "$(dirname {output.json})" "$(dirname {log})" "{params.benchdir}"

        PYTHONPATH="{params.pythonpath}" \
        python3 -m capstone.summarize \
            {params.unit_args} \
            {params.qc_raw_args} \
            {params.trim_args} \
            {params.qc_trimmed_args} \
            {params.dedup_args} \
            {params.kmer_args} \
            {params.screen_args} \
            --out-json "{output.json}" \
            --out-tsv "{output.tsv}" 2> "{log}"
        """

# -----------------------------
# HTML report
# -----------------------------
rule report:
    input:
        json=rules.summarize.output.json
    output:
        html=f"{PUBLISH}/{V}/report/index.html"
    log:
        f"{LOGS}/report.log"
    benchmark:
        f"{BENCH}/report.txt"
    conda:
        config["_env_python"]
    params:
        benchdir=BENCH,
        pythonpath=PYTHONPATH,
    shell:
        r"""
        set -euo pipefail

        mkdir -p "$(dirname {output.html})" "$(dirname {log})" "{params.benchdir}"

        PYTHONPATH="{params.pythonpath}" \
        python3 -m capstone.report \
            --summary-json "{input.json}" \
            --out-html "{output.html}" 2> "{log}"
        """
