use std::rc::Rc; use std::sync::Mutex; use std::thread;
fn main(){ let value=Rc::new(Mutex::new(1)); let _=thread::spawn(move || value.lock()); }
