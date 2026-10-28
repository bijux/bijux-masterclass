use std::cell::RefCell; use std::sync::Arc; use std::thread;
fn main(){ let value=Arc::new(RefCell::new(3)); let copy=Arc::clone(&value); let _=thread::spawn(move || *copy.borrow()); }
