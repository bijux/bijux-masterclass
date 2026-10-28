use std::sync::Arc; use std::thread;
fn main(){ let data=Arc::new(vec![1]); let c=Arc::clone(&data); let _=thread::spawn(move || c.push(2)); }
