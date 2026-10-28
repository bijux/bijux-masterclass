use std::thread;
fn main(){ let h=thread::spawn(||1); let _=h.join(); let _=h.join(); }
