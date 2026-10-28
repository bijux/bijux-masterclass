use std::collections::BTreeMap;
macro_rules! map { ($( $k:expr => $v:expr ),* $(,)?) => {{ let mut m=BTreeMap::new(); $(m.insert($k,$v);)* m }}; }
fn main() { let m=map!("a"=>1,"b"=>2,); assert_eq!(m.len(),2); }
