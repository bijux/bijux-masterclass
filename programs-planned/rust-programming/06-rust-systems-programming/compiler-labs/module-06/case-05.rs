#![allow(dead_code, unused_imports, unused_variables)]
use std::mem::MaybeUninit; fn main(){let slot=MaybeUninit::<String>::uninit();let _=slot.assume_init();}
