use std::collections::BTreeMap;
fn main(){ let mut m=BTreeMap::new(); m.insert("z",1); m.insert("a",2); assert_eq!(m.keys().copied().collect::<Vec<_>>(),vec!["a","z"]); }
