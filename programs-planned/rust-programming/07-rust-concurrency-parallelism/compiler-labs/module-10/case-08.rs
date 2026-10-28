use std::sync::Arc; use std::thread;
fn main(){ let v=Arc::new(Vec::<u8>::new()); let c=Arc::clone(&v); let _=thread::spawn(move || c.push(1)); }
