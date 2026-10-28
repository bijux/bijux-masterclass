use std::cell::Cell;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Phase {
    Parse,
    Expand,
    Resolve,
    TypeCheck,
    TraitSolve,
    BorrowCheck,
    Runtime,
    CodegenReview,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum ClaimKind {
    LanguageRule,
    CompilerDiagnostic,
    RuntimeObservation,
    ArtifactObservation,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Evidence {
    pub claim: String,
    pub phase: Phase,
    pub kind: ClaimKind,
    pub conclusion: &'static str,
    pub remains_unknown: &'static str,
}

pub fn classify(claim: &str) -> Evidence {
    let (phase, kind, conclusion, remains_unknown) = match claim {
        "overlapping mutable borrows" => (
            Phase::BorrowCheck,
            ClaimKind::LanguageRule,
            "the access pattern is rejected",
            "which product redesign is best",
        ),
        "unsatisfied projection equality" => (
            Phase::TraitSolve,
            ClaimKind::CompilerDiagnostic,
            "the requested associated types do not normalize to one type",
            "whether an explicit conversion belongs in the product",
        ),
        "drop output order" => (
            Phase::Runtime,
            ClaimKind::RuntimeObservation,
            "this execution produced the recorded destruction order",
            "the optimized instruction shape",
        ),
        "symbol size" => (
            Phase::CodegenReview,
            ClaimKind::ArtifactObservation,
            "the pinned artifact contains the observed symbol",
            "future toolchains, profiles, features, and targets",
        ),
        _ => (
            Phase::TypeCheck,
            ClaimKind::CompilerDiagnostic,
            "the claim needs a smaller causal specimen",
            "the first decisive rule",
        ),
    };

    Evidence {
        claim: claim.to_owned(),
        phase,
        kind,
        conclusion,
        remains_unknown,
    }
}

pub struct DropProbe<'a> {
    drops: &'a Cell<usize>,
}

impl Drop for DropProbe<'_> {
    fn drop(&mut self) {
        self.drops.set(self.drops.get() + 1);
    }
}

pub fn move_and_drop(drops: &Cell<usize>) -> usize {
    let first = DropProbe { drops };
    let second = DropProbe { drops };
    let pair = (first, second);
    drop(pair);
    drops.get()
}

pub fn early_return(drops: &Cell<usize>, return_early: bool) -> usize {
    let _first = DropProbe { drops };
    if return_early {
        return drops.get();
    }
    let _second = DropProbe { drops };
    drops.get()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn distinguishes_artifact_evidence() {
        let evidence = classify("symbol size");
        assert_eq!(evidence.kind, ClaimKind::ArtifactObservation);
        assert_eq!(evidence.phase, Phase::CodegenReview);
    }

    #[test]
    fn unknown_claim_requests_isolation() {
        let evidence = classify("the program is slow");
        assert_eq!(evidence.conclusion, "the claim needs a smaller causal specimen");
    }

    #[test]
    fn both_owned_values_drop() {
        let drops = Cell::new(0);
        assert_eq!(move_and_drop(&drops), 2);
    }

    #[test]
    fn early_return_still_destroys_live_locals() {
        let drops = Cell::new(0);
        let observed_inside = early_return(&drops, true);
        assert_eq!(observed_inside, 0);
        assert_eq!(drops.get(), 1);
    }
}
