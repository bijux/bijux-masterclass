use std::sync::Arc; use std::thread;
fn main(){ let v=Arc::new(vec![1,2,3]); let w=Arc::clone(&v); let h=thread::spawn(move || w.len()); assert_eq!(h.join().ok(),Some(3)); }
