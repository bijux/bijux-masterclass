macro_rules! pair { ($left:expr => $right:expr) => { ($left, $right) }; }
fn main() { let _ = pair!(1, 2); }
