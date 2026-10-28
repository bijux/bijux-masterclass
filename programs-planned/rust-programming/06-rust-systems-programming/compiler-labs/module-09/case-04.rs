#![allow(dead_code, unused_imports, unused_variables)]
use std::ffi::c_void; unsafe extern "C" fn increment(context:*mut c_void){ // SAFETY: caller passes a live `usize` pointer.
 unsafe{*context.cast::<usize>()+=1;}} fn main(){let mut count=0_usize; // SAFETY: context points to `count` for the call.
 unsafe{increment((&raw mut count).cast())};assert_eq!(count,1);}
