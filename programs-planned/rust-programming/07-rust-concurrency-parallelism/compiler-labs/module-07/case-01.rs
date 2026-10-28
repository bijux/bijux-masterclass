use std::sync::atomic::{AtomicUsize,Ordering};
fn main(){ let n=AtomicUsize::new(0); n.fetch_add(1,Ordering::Relaxed); assert_eq!(n.load(Ordering::Relaxed),1); }
