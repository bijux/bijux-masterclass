use std::thread;
fn main(){ let h=thread::spawn(|| panic!("worker")); assert!(h.join().is_err()); }
