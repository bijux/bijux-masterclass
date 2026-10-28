use std::thread;
fn main(){ let h=thread::spawn(|| 21*2); assert_eq!(h.join().ok(),Some(42)); }
