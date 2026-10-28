macro_rules! typed_pair { ($ty:ty; $a:expr, $b:expr) => { { let value: ($ty,$ty)=($a,$b); value } }; }
fn main() { assert_eq!(typed_pair!(u32; 1, 2), (1,2)); }
