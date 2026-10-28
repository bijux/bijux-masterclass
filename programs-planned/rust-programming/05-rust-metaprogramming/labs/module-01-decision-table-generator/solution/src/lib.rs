#![forbid(unsafe_code)]

macro_rules! criteria {
    ($( $variant:ident => ($label:literal, $explanation:literal) ),+ $(,)?) => {
        #[derive(Debug, Clone, Copy, PartialEq, Eq)]
        pub enum Criterion {
            $( $variant ),+
        }

        impl Criterion {
            pub const fn label(self) -> &'static str {
                match self {
                    $( Self::$variant => $label ),+
                }
            }

            pub const fn explanation(self) -> &'static str {
                match self {
                    $( Self::$variant => $explanation ),+
                }
            }
        }

        pub const ALL_CRITERIA: &[Criterion] = &[
            $( Criterion::$variant ),+
        ];
    };
}

criteria! {
    RuntimeBehavior => (
        "runtime behavior",
        "values and effects are known only while the program runs"
    ),
    ExistingItemShape => (
        "existing item shape",
        "a declared struct or enum is the source of truth"
    ),
    AttachedItemContract => (
        "attached item",
        "one function or item must be validated and augmented"
    ),
    BoundedTokenGrammar => (
        "bounded token grammar",
        "a small token-local relationship produces Rust syntax"
    ),
    RichCustomGrammar => (
        "rich custom grammar",
        "cross-entry validation requires a parsed semantic model"
    ),
    CheckedExternalInput => (
        "checked external input",
        "a file known before compilation becomes generated Rust"
    ),
}

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
    BoundedTokens,
    CustomSyntax,
    ExternalFile,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Problem {
    pub owner: InputOwner,
    pub cross_entry_validation: bool,
    pub several_rust_surfaces: bool,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Decision {
    pub mechanism: Mechanism,
    pub reason: &'static str,
}

pub fn recommend(problem: Problem) -> Result<Decision, &'static str> {
    let decision = match problem.owner {
        InputOwner::RuntimeValues => Decision {
            mechanism: Mechanism::OrdinaryRust,
            reason: "runtime values belong in functions or data",
        },
        InputOwner::ExistingItem => Decision {
            mechanism: Mechanism::Derive,
            reason: "the existing item shape is the source of truth",
        },
        InputOwner::AttachedItem => Decision {
            mechanism: Mechanism::Attribute,
            reason: "one attached item must be validated or augmented",
        },
        InputOwner::ExternalFile => Decision {
            mechanism: Mechanism::BuildScript,
            reason: "checked external data must become Rust before compilation",
        },
        InputOwner::BoundedTokens if !problem.cross_entry_validation => Decision {
            mechanism: Mechanism::DeclarativeMacro,
            reason: "the grammar is token-local and bounded",
        },
        InputOwner::BoundedTokens => {
            return Err(
                "bounded declarative syntax contradicts cross-entry semantic validation",
            );
        }
        InputOwner::CustomSyntax => Decision {
            mechanism: Mechanism::FunctionLikeProcMacro,
            reason: "a parsed custom grammar owns cross-entry rules",
        },
    };

    if !problem.several_rust_surfaces
        && matches!(decision.mechanism, Mechanism::DeclarativeMacro)
    {
        return Ok(Decision {
            mechanism: Mechanism::OrdinaryRust,
            reason: "one ordinary table is already a single source of truth",
        });
    }

    Ok(decision)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn criteria_are_ordered() {
        assert_eq!(ALL_CRITERIA[0].label(), "runtime behavior");
        assert_eq!(ALL_CRITERIA.len(), 6);
    }

    #[test]
    fn runtime_is_ordinary() {
        let decision = recommend(Problem {
            owner: InputOwner::RuntimeValues,
            cross_entry_validation: false,
            several_rust_surfaces: false,
        })
        .expect("runtime decision");
        assert_eq!(decision.mechanism, Mechanism::OrdinaryRust);
    }

    #[test]
    fn bounded_tokens_need_multiple_surfaces() {
        let decision = recommend(Problem {
            owner: InputOwner::BoundedTokens,
            cross_entry_validation: false,
            several_rust_surfaces: false,
        })
        .expect("bounded-token decision");
        assert_eq!(decision.mechanism, Mechanism::OrdinaryRust);
    }

    #[test]
    fn contradictory_problem_is_rejected() {
        let result = recommend(Problem {
            owner: InputOwner::BoundedTokens,
            cross_entry_validation: true,
            several_rust_surfaces: true,
        });
        assert!(result.is_err());
    }
}
