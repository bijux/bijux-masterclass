use std::thread;
fn main() { let text=String::from("owned"); let h=thread::spawn(move || text.len()); assert_eq!(h.join().ok(), Some(5)); }
