#![allow(dead_code, unused_imports, unused_variables)]
fn main(){let source=[1_u8,2];let mut destination=[0_u8;2];std::ptr::copy_nonoverlapping(source.as_ptr(),destination.as_mut_ptr(),2);}
