#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Decision {
    pub requirement: &'static str,
    pub mechanism: &'static str,
    pub proof_owner: &'static str,
}

pub const BASELINE: Decision = Decision {
    requirement: "stable artifact identity",
    mechanism: "validated versioned header",
    proof_owner: "decoder and golden fixtures",
};

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn baseline_decision_names_an_owner() {
        assert!(!BASELINE.proof_owner.is_empty());
    }
}
