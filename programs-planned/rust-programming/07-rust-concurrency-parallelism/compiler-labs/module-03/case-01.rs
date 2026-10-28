use std::sync::{Arc,Mutex}; use std::thread;
fn main(){ let v=Arc::new(Mutex::new(0usize)); let c=Arc::clone(&v); let h=thread::spawn(move || { if let Ok(mut g)=c.lock(){*g+=1;} }); let _=h.join(); }
