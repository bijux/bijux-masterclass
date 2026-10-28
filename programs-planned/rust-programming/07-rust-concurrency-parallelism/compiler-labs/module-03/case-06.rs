use std::sync::{Mutex,MutexGuard};
fn bad() -> MutexGuard<'static,i32>{ let m=Mutex::new(1); m.lock().unwrap() }
fn main(){ let _=bad(); }
