#![allow(dead_code, unused_imports, unused_variables)]
use std::mem::MaybeUninit; fn main(){ let mut slot=MaybeUninit::<String>::uninit(); let _ = slot.write(String::from("ready")); // SAFETY: `write` initialized the slot exactly once.
 let value=unsafe{slot.assume_init()}; assert_eq!(value,"ready"); }
