#![forbid(unsafe_code)]

//! BatchWeave is a bounded, deterministic concurrent batch engine used by
//! Course 7 of the reader-first Rust program.

pub mod app;
pub mod domain;
pub mod engine;
pub mod error;
pub mod metrics;
pub mod operations;
pub mod parse;
pub mod report;
mod queue;

pub use app::{AppOutput, run_arguments};
pub use domain::{
    EngineConfig, FailurePolicy, Job, JobId, JobOutcome, Operation, OutcomeKind,
    RunReport, Summary,
};
pub use engine::run_jobs;
pub use error::{AppError, DomainError, ManifestError, RunError};
pub use parse::parse_manifest;
pub use report::{render_inspection, render_report, report_is_accepted, summarize_sequential};
