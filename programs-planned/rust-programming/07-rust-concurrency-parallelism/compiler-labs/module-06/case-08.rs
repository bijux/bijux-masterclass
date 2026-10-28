use std::sync::Barrier; use std::thread;
fn main(){ let b=Barrier::new(2); let _a=thread::spawn(move || {b.wait();}); let _b=thread::spawn(move || {b.wait();}); }
