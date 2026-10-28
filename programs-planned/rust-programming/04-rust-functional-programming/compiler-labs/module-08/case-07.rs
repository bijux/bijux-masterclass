use std::collections::BTreeSet;
fn main(){let mut s=BTreeSet::new();s.insert(1);let once=s.clone();s.insert(1);assert_eq!(s,once);}
