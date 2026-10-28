#![allow(dead_code, unused_imports, unused_variables)]
type Callback=unsafe extern "C" fn(*const u8)->i32; unsafe extern "C" fn cb(pointer:*const u8)->i32{if pointer.is_null(){1}else{0}} fn invoke(callback:Callback,pointer:*const u8)->i32{ // SAFETY: callback contract accepts this pointer for the duration of the call.
 unsafe{callback(pointer)}} fn main(){let value=1_u8;assert_eq!(invoke(cb,&raw const value),0);}
