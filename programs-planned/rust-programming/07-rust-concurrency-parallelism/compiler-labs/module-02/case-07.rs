use std::thread;
fn main(){ let value: &str = thread::scope(|s| s.spawn(|| { let text=String::from("local"); text.as_str() }).join().unwrap()); println!("{value}"); }
