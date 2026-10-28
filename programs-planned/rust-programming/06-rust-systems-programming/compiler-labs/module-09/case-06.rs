#![allow(dead_code, unused_imports, unused_variables)]
type Callback=unsafe extern "C" fn(*const u8); unsafe extern "C" fn cb(_: *const u8){} fn main(){let callback:Callback=cb;callback(std::ptr::null());}
