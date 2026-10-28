use std::sync::{Arc,Barrier}; use std::thread;
fn main(){ let b=Arc::new(Barrier::new(2)); let c=Arc::clone(&b); let h=thread::spawn(move || {c.wait();}); b.wait(); let _=h.join(); }
