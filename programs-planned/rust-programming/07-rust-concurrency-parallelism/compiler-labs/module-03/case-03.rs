use std::sync::Mutex;
fn main(){ let m=Mutex::new(1); let value={ let g=m.lock().expect("lock"); *g }; println!("{value}"); }
