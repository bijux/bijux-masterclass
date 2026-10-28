use std::thread;
fn main(){ let h=thread::spawn(||1); let _copy=h.clone(); }
