use std::sync::mpsc; use std::thread;
fn main(){ let text=String::from("local"); let (tx,_rx)=mpsc::channel::<&str>(); let _=thread::spawn(move || tx.send(text.as_str())); }
