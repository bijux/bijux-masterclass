#![forbid(unsafe_code)]

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Mechanism {
    OrdinaryRust,
    DeclarativeMacro,
    Derive,
    Attribute,
    FunctionLikeProcMacro,
    BuildScript,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum InputOwner {
    RuntimeValues,
    ExistingItem,
    AttachedItem,
    CustomSyntax,
    ExternalFile,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Problem {
    pub owner: InputOwner,
    pub cross_entry_validation: bool,
    pub several_rust_surfaces: bool,
}

pub fn baseline(problem: Problem) -> Mechanism {
    match problem.owner {
        InputOwner::RuntimeValues => Mechanism::OrdinaryRust,
        InputOwner::ExistingItem => Mechanism::Derive,
        InputOwner::AttachedItem => Mechanism::Attribute,
        InputOwner::CustomSyntax => Mechanism::FunctionLikeProcMacro,
        InputOwner::ExternalFile => Mechanism::BuildScript,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn runtime_values_stay_ordinary() {
        assert_eq!(
            baseline(Problem {
                owner: InputOwner::RuntimeValues,
                cross_entry_validation: false,
                several_rust_surfaces: false,
            }),
            Mechanism::OrdinaryRust,
        );
    }
}
