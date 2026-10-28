use std::sync::{Condvar,Mutex}; use std::time::Duration;
fn main(){ let m=Mutex::new(false); let c=Condvar::new(); let g=m.lock().expect("lock"); let (_g,_status)=c.wait_timeout(g,Duration::from_millis(1)).expect("wait"); }
