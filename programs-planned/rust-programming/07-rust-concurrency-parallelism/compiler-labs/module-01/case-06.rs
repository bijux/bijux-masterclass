use std::rc::Rc; use std::thread;
fn main(){ let value=Rc::new(3); let _=thread::spawn(move || *value); }
