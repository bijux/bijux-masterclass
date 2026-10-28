mod support { pub fn value()->u32{7} }
macro_rules! value {()=>{$crate::support::value()};}
fn main(){assert_eq!(value!(),7);}
