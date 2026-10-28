use std::sync::mpsc;
fn main(){ let (tx,_rx)=mpsc::channel(); let job=String::from("job"); tx.send(job).ok(); println!("{job}"); }
