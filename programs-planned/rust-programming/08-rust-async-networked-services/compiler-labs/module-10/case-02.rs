#![allow(dead_code)]
use std::sync::{Arc, atomic::{AtomicUsize, Ordering}};
fn main() { let active = Arc::new(AtomicUsize::new(0)); let observer = Arc::clone(&active); active.fetch_add(1, Ordering::Relaxed); assert_eq!(observer.load(Ordering::Relaxed),1); }
