#![forbid(unsafe_code)]
//! Starter for the boundary-ports laboratory.

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Item { pub id: u64, pub value: i32 }

pub struct MemorySource { items: Vec<Item> }
impl MemorySource { pub fn new(items: Vec<Item>) -> Self { Self { items } } pub fn len(&self)->usize{self.items.len()} }

#[cfg(test)] mod tests { use super::*; #[test] fn stores_items(){assert_eq!(MemorySource::new(vec![Item{id:1,value:2}]).len(),1);} }
