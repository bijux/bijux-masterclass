# Reference — Progressive-delivery math

Configured weight is not observed exposure. Record candidate requests `n_c`, stable requests `n_s`, failure counts, latency distributions, and segment populations. Enforce a minimum `n_c` and a window longer than telemetry delay.

Use absolute thresholds and comparative thresholds. A simple relative error-rate test can be written as `candidate_rate <= stable_rate + margin`, but confidence and sample adequacy must be considered. Missing data has an explicit outcome.

## Extended reader notes

Let `n_c` and `n_s` be actual candidate and stable attempts, not configured weights. For a failure rate, record `f_c / n_c` and `f_s / n_s`, minimum sample counts, and the populations represented. An absolute rule such as `f_c/n_c <= 0.01` prevents both revisions being equally bad. A comparative rule such as `candidate <= stable + margin` detects regression relative to current conditions.

Tail latency requires distributions, not averages. Telemetry delay must be shorter than the analysis window, and the decision should wait for late samples. Segment analysis is necessary when the change affects one tenant, region, payload size, or endpoint differently. Retries must be visible as attempts and useful outcomes.

Course fixtures use deterministic thresholds rather than claiming statistical certification. In production, select a method appropriate to traffic volume and risk, record confidence or uncertainty, and classify insufficient evidence as inconclusive rather than success.
