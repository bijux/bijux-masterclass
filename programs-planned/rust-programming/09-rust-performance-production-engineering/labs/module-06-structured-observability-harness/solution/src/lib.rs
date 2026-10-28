use std::collections::BTreeMap;

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum Outcome {
    Accepted,
    RejectedInvalid,
    RejectedOverloaded,
    FailedInternal,
}

impl Outcome {
    pub const fn as_str(self) -> &'static str {
        match self {
            Self::Accepted => "accepted",
            Self::RejectedInvalid => "rejected_invalid",
            Self::RejectedOverloaded => "rejected_overloaded",
            Self::FailedInternal => "failed_internal",
        }
    }
}

#[derive(Clone, PartialEq, Eq)]
pub struct Secret(String);

impl Secret {
    pub fn new(value: String) -> Self {
        Self(value)
    }

    pub fn expose(&self) -> &str {
        &self.0
    }
}

impl std::fmt::Debug for Secret {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        formatter.write_str("Secret([REDACTED])")
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Event {
    pub name: &'static str,
    pub request_id: u64,
    pub operation: &'static str,
    pub outcome: Outcome,
    pub fields: BTreeMap<&'static str, u64>,
}

#[derive(Debug, Default)]
pub struct Metrics {
    outcomes: BTreeMap<Outcome, u64>,
    queue_depth_observed: usize,
}

impl Metrics {
    pub fn record(&mut self, event: &Event) {
        *self.outcomes.entry(event.outcome).or_default() += 1;
        if let Some(depth) = event.fields.get("queue_depth") {
            self.queue_depth_observed = usize::try_from(*depth).unwrap_or(usize::MAX);
        }
    }

    pub fn outcome_count(&self, outcome: Outcome) -> u64 {
        self.outcomes.get(&outcome).copied().unwrap_or_default()
    }

    pub fn queue_depth_observed(&self) -> usize {
        self.queue_depth_observed
    }
}

#[tracing::instrument(
    name = "handle_request",
    skip(secret),
    fields(request_id, operation, outcome = tracing::field::Empty)
)]
pub fn handle(request_id: u64, operation: &'static str, secret: &Secret, overloaded: bool) -> Event {
    let _secret_is_available_to_domain_logic = secret.expose();
    let outcome = if overloaded {
        Outcome::RejectedOverloaded
    } else {
        Outcome::Accepted
    };
    tracing::Span::current().record("outcome", outcome.as_str());
    let queue_depth = if overloaded { 1 } else { 0 };
    tracing::info!(queue_depth, "request decision");
    Event {
        name: "request_decision",
        request_id,
        operation,
        outcome,
        fields: BTreeMap::from([("queue_depth", queue_depth)]),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn outcome_labels_are_bounded_and_counted() {
        let secret = Secret::new("token".into());
        let event = handle(9, "ingest", &secret, true);
        let mut metrics = Metrics::default();
        metrics.record(&event);
        assert_eq!(metrics.outcome_count(Outcome::RejectedOverloaded), 1);
        assert_eq!(metrics.queue_depth_observed(), 1);
    }

    #[test]
    fn secret_debug_is_redacted() {
        let secret = Secret::new("top-secret".into());
        assert_eq!(format!("{secret:?}"), "Secret([REDACTED])");
        let event = handle(1, "snapshot", &secret, false);
        assert!(!format!("{event:?}").contains("top-secret"));
    }

    #[test]
    fn event_schema_is_stable() {
        let event = handle(42, "ingest", &Secret::new("x".into()), false);
        assert_eq!(event.name, "request_decision");
        assert_eq!(event.operation, "ingest");
        assert_eq!(event.outcome.as_str(), "accepted");
    }
}
