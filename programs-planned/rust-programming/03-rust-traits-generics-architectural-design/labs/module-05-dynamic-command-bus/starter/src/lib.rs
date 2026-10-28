#![forbid(unsafe_code)]
//! Starter for the dynamic-command-bus laboratory.

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Command { pub name: String, pub payload: String }
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Response(pub String);

pub struct Bus<'a> { _marker: std::marker::PhantomData<&'a ()> }
impl<'a> Bus<'a> { pub fn new() -> Self { Self { _marker: std::marker::PhantomData } } }
impl Default for Bus<'_> { fn default() -> Self { Self::new() } }

#[cfg(test)] mod tests { use super::*; #[test] fn creates_bus(){ let _=Bus::new(); } }
