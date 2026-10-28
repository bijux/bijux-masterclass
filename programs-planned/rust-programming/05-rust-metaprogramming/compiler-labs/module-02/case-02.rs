macro_rules! literal_only { ($value:literal) => { $value }; }
fn main() { let _ = literal_only!(1 + 2); }
