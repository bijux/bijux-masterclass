use std::sync::{Condvar,Mutex};
fn main(){ let m=Mutex::new(false); let c=Condvar::new(); let mut g=m.lock().unwrap(); let _=c.wait(&mut g); }
