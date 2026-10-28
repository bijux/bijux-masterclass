use std::sync::Condvar; use std::thread;
fn main(){ let c=Condvar::new(); let _a=thread::spawn(move || c.notify_all()); let _b=thread::spawn(move || c.notify_all()); }
