macro_rules! twice_value { ($value:expr) => {{ let captured=$value; (captured, captured) }}; }
fn main() { let mut n=0; let p=twice_value!({n+=1;n}); assert_eq!((p,n),((1,1),1)); }
