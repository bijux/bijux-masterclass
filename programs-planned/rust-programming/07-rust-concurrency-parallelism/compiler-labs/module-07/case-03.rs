use std::sync::atomic::{AtomicUsize,Ordering};
fn main(){ let n=AtomicUsize::new(1); let _=n.compare_exchange(1,0,Ordering::AcqRel,Ordering::Relaxed); }
