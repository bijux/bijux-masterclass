#![allow(dead_code, unused_imports, unused_variables)]
use std::mem::ManuallyDrop; fn main(){let mut value=ManuallyDrop::new(String::from("owned")); // SAFETY: this is the only destruction of the initialized inner String.
 unsafe{ManuallyDrop::drop(&mut value);}}
