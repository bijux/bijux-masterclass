use std::thread;
fn main(){ let text=String::from("moved"); let h=thread::spawn(move || text.len()); println!("{text}"); let _=h.join(); }
