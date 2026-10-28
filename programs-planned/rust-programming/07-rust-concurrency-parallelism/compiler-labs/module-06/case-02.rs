use std::sync::atomic::{AtomicBool,Ordering};
fn main(){ let c=AtomicBool::new(false); c.store(true,Ordering::Relaxed); assert!(c.load(Ordering::Relaxed)); }
