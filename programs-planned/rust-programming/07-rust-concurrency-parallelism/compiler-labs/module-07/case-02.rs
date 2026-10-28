use std::sync::atomic::{AtomicBool,Ordering};
fn main(){ let ready=AtomicBool::new(false); ready.store(true,Ordering::Release); assert!(ready.load(Ordering::Acquire)); }
