use std::thread;
struct Producer;
fn main(){ let p=Producer; let h=thread::spawn(move || {let _=p;}); let _=h.join(); }
