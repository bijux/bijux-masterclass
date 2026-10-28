use std::cell::UnsafeCell; use std::sync::Arc; use std::thread;
fn main(){ let c=Arc::new(UnsafeCell::new(1)); let d=Arc::clone(&c); let _=thread::spawn(move || d.get()); }
