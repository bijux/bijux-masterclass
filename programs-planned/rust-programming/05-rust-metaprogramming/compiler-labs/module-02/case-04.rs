macro_rules! broken { ($( $name:ident ),*) => { stringify!($name) }; }
fn main() { let _ = broken!(a, b); }
