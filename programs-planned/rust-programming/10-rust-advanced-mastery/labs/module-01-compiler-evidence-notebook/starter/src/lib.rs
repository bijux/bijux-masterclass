#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Phase {
    Parse,
    Resolve,
    TypeCheck,
    BorrowCheck,
    Runtime,
    CodegenReview,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Evidence {
    pub claim: &'static str,
    pub phase: Phase,
    pub conclusion: &'static str,
}

pub fn phase_for_borrow_conflict() -> Phase {
    Phase::BorrowCheck
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn borrow_conflicts_have_a_distinct_phase() {
        assert_eq!(phase_for_borrow_conflict(), Phase::BorrowCheck);
    }
}
