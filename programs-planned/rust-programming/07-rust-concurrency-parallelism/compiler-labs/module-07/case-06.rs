#![deny(invalid_atomic_ordering)]
use std::sync::atomic::{AtomicUsize,Ordering};
fn main(){ let n=AtomicUsize::new(0); n.store(1,Ordering::Acquire); }
