#![forbid(unsafe_code)]
//! Starter for the composed-renderer laboratory.

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Report { pub title: String, pub lines: Vec<String> }

pub struct Plain;

#[cfg(test)] mod tests { use super::*; #[test] fn report_holds_lines(){ assert_eq!(Report{title:"x".into(),lines:vec!["a".into()]}.lines.len(),1); } }
