use std::panic;
fn main(){ let result=panic::catch_unwind(|| panic!("job")); assert!(result.is_err()); }
