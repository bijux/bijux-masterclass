use std::sync::{Condvar,Mutex};
fn main(){ let pair=(Mutex::new(true),Condvar::new()); let (m,c)=(&pair.0,&pair.1); let mut g=m.lock().expect("lock"); while !*g { g=c.wait(g).expect("wait"); } }
