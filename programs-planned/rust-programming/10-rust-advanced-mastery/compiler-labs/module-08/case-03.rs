use std::collections::BTreeMap;fn main(){let mut m=BTreeMap::new();m.insert("a",1);assert_eq!(m.remove("a"),Some(1));}
