use std::thread;
fn main(){ let handle=thread::scope(|s| s.spawn(|| 1)); let _=handle.join(); }
