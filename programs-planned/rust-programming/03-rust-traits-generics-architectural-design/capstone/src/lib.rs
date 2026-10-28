#![forbid(unsafe_code)]
//! A deterministic policy-driven submission review engine.
//!
//! The crate intentionally demonstrates several distinct polymorphism choices.
//! Sources and reporters remain generic; heterogeneous rules are erased behind
//! [`Rule`] objects; [`EngineBuilder`] uses typestate only during construction.

pub mod domain;
pub mod engine;
pub mod error;
pub mod policy;
pub mod reporter;
pub mod rule;
pub mod source;

pub use domain::{Finding, Review, RuleId, Severity, Submission, SubmissionId};
pub use engine::{Engine, EngineBuilder, Missing, Present, RunOutcome};
pub use error::{InputError, PolicyError, ReportError, RunError};
pub use policy::{default_registry, Policy, RuleFactory, RuleRegistry};
pub use reporter::{Reporter, TextReporter, TsvReporter};
pub use rule::{BuiltInRule, EvaluationContext, Rule, RuleExt, RuleFn};
pub use source::{FileSource, MemorySource, Source, TsvSource};
