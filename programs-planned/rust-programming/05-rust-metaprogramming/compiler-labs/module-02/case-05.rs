macro_rules! ambiguous { ($($head:ident)* $tail:ident) => { () }; }
fn main() { ambiguous!(only); }
