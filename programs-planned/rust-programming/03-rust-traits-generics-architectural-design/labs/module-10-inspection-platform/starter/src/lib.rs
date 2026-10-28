#![forbid(unsafe_code)]
//! Starter for the inspection-platform transfer laboratory.

#[derive(Clone,Debug,PartialEq,Eq)]
pub struct Sample{pub id:u64,pub reading:i32}
#[derive(Clone,Copy,Debug,PartialEq,Eq)]
pub enum Level{Info,Warning,Error}

#[cfg(test)]mod tests{use super::*;#[test]fn level_is_closed_domain(){assert_eq!(Level::Error,Level::Error);}}
