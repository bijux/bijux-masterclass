use std::sync::atomic::{AtomicUsize,Ordering};
fn main(){ let q=AtomicUsize::new(2); assert!(q.fetch_update(Ordering::Relaxed,Ordering::Relaxed,|n| n.checked_sub(1)).is_ok()); }
