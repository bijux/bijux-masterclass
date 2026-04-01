# workflow/rules/preprocess.smk
from __future__ import annotations

RESULTS = config["results_dir"]
LOGS = config["logs_dir"]
BENCH = config["benchmarks_dir"]

# -----------------------------
# Modules
# -----------------------------
module qc:
    snakefile: "../modules/qc_module/Snakefile"
    config: config

use rule qc from qc as qc_raw with:
    input:
        fastq=lambda wc: get_raw_fastq(wc)
    output:
        json=f"{RESULTS}/{{sample}}/qc_raw.json",
        tsv=f"{RESULTS}/{{sample}}/qc_raw.tsv",
    log:
        f"{LOGS}/{{sample}}/qc_raw.log"
    benchmark:
        f"{BENCH}/qc_raw_{{sample}}.txt"
    resources:
        mem_mb=lambda wc, input: max(1000, int(1.5 * file_size_mb(input.fastq)) + 500)

use rule qc from qc as qc_trimmed with:
    input:
        fastq=f"{RESULTS}/{{sample}}/trimmed.fastq.gz"
    output:
        json=f"{RESULTS}/{{sample}}/qc_trimmed.json",
        tsv=f"{RESULTS}/{{sample}}/qc_trimmed.tsv",
    log:
        f"{LOGS}/{{sample}}/qc_trimmed.log"
    benchmark:
        f"{BENCH}/qc_trimmed_{{sample}}.txt"
    resources:
        mem_mb=lambda wc, input: max(1000, int(1.5 * file_size_mb(input.fastq)) + 500)

module screen:
    snakefile: "../modules/screen_module/Snakefile"
    config: config

use rule screen from screen as screen_panel with:
    input:
        kmer_json=f"{RESULTS}/{{sample}}/kmer.json"
    output:
        json=f"{RESULTS}/{{sample}}/screen.json"
    params:
        panel_fasta=config["params"]["panel"]["fasta"]
    log:
        f"{LOGS}/{{sample}}/screen.log"
    benchmark:
        f"{BENCH}/screen_{{sample}}.txt"
    resources:
        mem_mb=500

# -----------------------------
# Trimming
# -----------------------------
rule trim_fastq:
    input:
        fastq=lambda wc: get_raw_fastq(wc)
    output:
        fastq=f"{RESULTS}/{{sample}}/trimmed.fastq.gz",
        json=f"{RESULTS}/{{sample}}/trim.json",
    log:
        f"{LOGS}/{{sample}}/trim.log"
    benchmark:
        f"{BENCH}/trim_{{sample}}.txt"
    conda:
        config["_env_python"]
    resources:
        mem_mb=lambda wc, input: max(2000, int(1.5 * file_size_mb(input.fastq)) + 1000)
    params:
        q=config["params"]["trim"]["q"],
        min_len=config["params"]["trim"]["min_len"],
        max_n_fraction=config["params"]["trim"]["max_n_fraction"],
        adapters_fasta=config["params"]["trim"]["adapters_fasta"],
        adapter_min_overlap=config["params"]["trim"]["adapter_min_overlap"],
        poly_run_min=config["params"]["trim"]["poly_run_min"],
        pythonpath=PYTHONPATH,
        benchdir=BENCH,
    shell:
        r"""
        set -euo pipefail

        mkdir -p "$(dirname {output.fastq})" "$(dirname {log})" "{params.benchdir}"

        echo "Resolved resources:" > "{log}"
        echo " mem_mb={resources.mem_mb}" >> "{log}"
        echo " input_size_mb=$(du -m "{input.fastq}" | cut -f1)" >> "{log}"

        PYTHONPATH="{params.pythonpath}" \
        python3 -m capstone.trim_fastq \
            --in-fastq "{input.fastq}" \
            --out-fastq "{output.fastq}" \
            --out-json "{output.json}" \
            --q {params.q} \
            --min-len {params.min_len} \
            --max-n-fraction {params.max_n_fraction} \
            --adapters-fasta "{params.adapters_fasta}" \
            --adapter-min-overlap {params.adapter_min_overlap} \
            --poly-run-min {params.poly_run_min} 2>> "{log}"
        """

# -----------------------------
# Deduplication
# -----------------------------
rule dedup_fastq:
    input:
        fastq=f"{RESULTS}/{{sample}}/trimmed.fastq.gz"
    output:
        fastq=f"{RESULTS}/{{sample}}/dedup.fastq.gz",
        json=f"{RESULTS}/{{sample}}/dedup.json",
    log:
        f"{LOGS}/{{sample}}/dedup.log"
    benchmark:
        f"{BENCH}/dedup_{{sample}}.txt"
    conda:
        config["_env_python"]
    resources:
        mem_mb=lambda wc, input: max(4000, int(1.5 * file_size_mb(input.fastq)) + 2000)
    params:
        mode=config["params"]["dedup"]["mode"],
        pythonpath=PYTHONPATH,
        benchdir=BENCH,
    shell:
        r"""
        set -euo pipefail

        mkdir -p "$(dirname {output.fastq})" "$(dirname {log})" "{params.benchdir}"

        echo "Resolved resources:" > "{log}"
        echo " mem_mb={resources.mem_mb}" >> "{log}"
        echo " input_size_mb=$(du -m "{input.fastq}" | cut -f1)" >> "{log}"

        PYTHONPATH="{params.pythonpath}" \
        python3 -m capstone.dedup_fastq \
            --mode {params.mode} \
            --in-fastq "{input.fastq}" \
            --out-fastq "{output.fastq}" \
            --out-json "{output.json}" 2>> "{log}"
        """

# -----------------------------
# k-mer profiling
# -----------------------------
rule kmer_profile:
    input:
        fastq=f"{RESULTS}/{{sample}}/dedup.fastq.gz"
    output:
        json=f"{RESULTS}/{{sample}}/kmer.json"
    log:
        f"{LOGS}/{{sample}}/kmer.log"
    benchmark:
        f"{BENCH}/kmer_{{sample}}.txt"
    conda:
        config["_env_python"]
    resources:
        mem_mb=lambda wc, input: max(2000, int(1.5 * file_size_mb(input.fastq)) + 1000)
    params:
        k=config["params"]["kmer"]["k"],
        signature_size=config["params"]["kmer"]["signature_size"],
        top=config["params"]["kmer"]["top"],
        pythonpath=PYTHONPATH,
        benchdir=BENCH,
    shell:
        r"""
        set -euo pipefail

        mkdir -p "$(dirname {output.json})" "$(dirname {log})" "{params.benchdir}"

        echo "Resolved resources:" > "{log}"
        echo " mem_mb={resources.mem_mb}" >> "{log}"
        echo " input_size_mb=$(du -m "{input.fastq}" | cut -f1)" >> "{log}"

        PYTHONPATH="{params.pythonpath}" \
        python3 -m capstone.kmer_profile \
            --in-fastq "{input.fastq}" \
            --out-json "{output.json}" \
            --k {params.k} \
            --signature-size {params.signature_size} \
            --top {params.top} 2>> "{log}"
        """
