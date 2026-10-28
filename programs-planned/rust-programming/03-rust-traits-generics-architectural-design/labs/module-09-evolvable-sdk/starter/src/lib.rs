#![forbid(unsafe_code)]
//! Starter for the evolvable-sdk laboratory.

pub trait PluginV1 { fn run(&self, input: &str) -> String; }
pub struct Upper;
impl PluginV1 for Upper { fn run(&self,input:&str)->String{input.to_uppercase()} }

#[cfg(test)] mod tests{use super::*;#[test]fn v1_runs(){assert_eq!(Upper.run("a"),"A");}}
