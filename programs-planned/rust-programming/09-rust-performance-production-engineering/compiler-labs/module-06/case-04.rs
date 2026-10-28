fn bucket(ms: u64) -> &'static str { match ms { 0..=9=>"lt10", 10..=99=>"lt100", _=>"ge100" } } fn main() { assert_eq!(bucket(42), "lt100"); }
