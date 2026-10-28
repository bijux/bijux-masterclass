use std::sync::Mutex; use std::thread;
fn main(){ let value=Mutex::new(1); let guard=value.lock().expect("lock"); let _=thread::spawn(move || *guard); }
