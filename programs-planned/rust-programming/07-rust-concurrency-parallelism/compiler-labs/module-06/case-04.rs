use std::sync::atomic::{AtomicBool,Ordering};
fn main(){ let closed=AtomicBool::new(false); closed.store(true,Ordering::Relaxed); closed.store(true,Ordering::Relaxed); }
