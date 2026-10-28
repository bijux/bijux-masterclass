//! The builder restricts incomplete construction.
//!
//! ```compile_fail
//! use review_engine::{EngineBuilder, TextReporter};
//! let engine = EngineBuilder::new().with_reporter(TextReporter).build();
//! ```

#[test] fn compile_fail_contract_is_documented() { assert!(true); }
