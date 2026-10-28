use std::sync::atomic::{AtomicBool,Ordering}; use std::thread;
fn main(){ let c=AtomicBool::new(false); let h=thread::spawn(move || c.store(true,Ordering::Relaxed)); let _=c.load(Ordering::Relaxed); let _=h.join(); }
