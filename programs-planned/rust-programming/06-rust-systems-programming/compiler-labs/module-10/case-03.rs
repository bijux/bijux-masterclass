#![allow(dead_code, unused_imports, unused_variables)]
fn boundary(action:impl FnOnce()->i32)->i32{std::panic::catch_unwind(std::panic::AssertUnwindSafe(action)).unwrap_or(9)} fn main(){assert_eq!(boundary(||panic!("x")),9);}
