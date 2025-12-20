# workflow/rules/publish.smk
from __future__ import annotations

PUBLISH = config["publish_dir"]
LOGS = config["logs_dir"]
BENCH = config["benchmarks_dir"]
V = config["params"]["publish"]["version"]

rule manifest:
    input:
        summary_json = rules.summarize.output.json,
        summary_tsv  = rules.summarize.output.tsv,
        report_html  = rules.report.output.html,
        provenance   = rules.provenance.output.json,
        discovered   = rules.publish_discovered_samples.output.json,
    output:
        json = f"{PUBLISH}/{V}/manifest.json",
    log:
        f"{LOGS}/manifest.log"
    benchmark:
        f"{BENCH}/manifest.txt"
    conda:
        config["_env_python"]
    params:
        pythonpath=PYTHONPATH,
        benchdir=BENCH,
    shell:
        r"""
        set -euo pipefail
        mkdir -p "$(dirname {output.json})" "$(dirname {log})" "{params.benchdir}"

        PYTHONPATH="{params.pythonpath}" \
        python3 -m capstone.manifest --out "{output.json}" \
            "{input.summary_json}" \
            "{input.summary_tsv}" \
            "{input.report_html}" \
            "{input.provenance}" \
            "{input.discovered}" 2> "{log}"
        """

