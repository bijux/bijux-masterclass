#![forbid(unsafe_code)]

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Leg {
    pub route: String,
    pub from: String,
    pub to: String,
    pub distance: u64,
    pub line: usize,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Diagnostic {
    FieldCount { line: usize },
    InvalidDistance { line: usize, value: String },
    EmptyRoute { route: String },
    Disconnected {
        route: String,
        line: usize,
        expected: String,
        found: String,
    },
    Overflow { route: String },
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RouteSummary {
    pub route: String,
    pub origin: String,
    pub destination: String,
    pub legs: usize,
    pub distance: u64,
}

#[cfg(test)]
mod tests {
    use super::{Leg, RouteSummary};

    #[test]
    fn starter_distinguishes_source_legs_from_route_summaries() {
        let leg = Leg {
            route: "r".to_owned(),
            from: "a".to_owned(),
            to: "b".to_owned(),
            distance: 4,
            line: 1,
        };
        let summary = RouteSummary {
            route: leg.route.clone(),
            origin: leg.from.clone(),
            destination: leg.to.clone(),
            legs: 1,
            distance: leg.distance,
        };
        assert_eq!(summary.origin, "a");
        assert_eq!(summary.distance, 4);
    }
}
