use std::thread;
fn main(){ let values=vec![1,2,3]; let _=thread::spawn(|| values.len()); }
