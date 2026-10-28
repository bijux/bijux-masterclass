use std::cell::RefCell; use std::panic;
fn main(){ let state=RefCell::new(1); let _=panic::catch_unwind(|| *state.borrow_mut()+=1); }
