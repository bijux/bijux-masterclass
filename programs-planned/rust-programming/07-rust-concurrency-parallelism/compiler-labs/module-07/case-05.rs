#![deny(invalid_atomic_ordering)]
use std::sync::atomic::{AtomicUsize,Ordering};
fn main(){ let n=AtomicUsize::new(0); let _=n.load(Ordering::Release); }
