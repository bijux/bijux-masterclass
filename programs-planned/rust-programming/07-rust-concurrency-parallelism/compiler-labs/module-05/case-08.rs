use std::sync::mpsc;
fn main(){ let (tx,_rx)=mpsc::channel::<u32>(); let _=tx.send("stop"); }
