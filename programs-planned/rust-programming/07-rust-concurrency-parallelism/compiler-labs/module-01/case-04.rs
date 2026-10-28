use std::sync::{Arc,Mutex}; use std::thread;
fn main(){ let n=Arc::new(Mutex::new(0)); let w=Arc::clone(&n); let h=thread::spawn(move || { if let Ok(mut g)=w.lock(){*g+=1;} }); let _=h.join(); }
