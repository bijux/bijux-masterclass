# Reports

`release-verification.json` is the machine-readable record of the executed and unexecuted evidence lanes for Course 5.

Generated experiment output is written under `capstone/reports/generated/` and is intentionally excluded from integrity manifests. Run `make capstone-tour` to reproduce it and `make clean` to remove it.

`FINAL-VERIFICATION.md` is the human-readable release summary. The ZIP checksum and external release record are published beside the final archive because an archive cannot safely contain a trustworthy digest of its own final bytes.
