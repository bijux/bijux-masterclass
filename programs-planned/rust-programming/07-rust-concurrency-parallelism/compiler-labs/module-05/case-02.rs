use std::sync::mpsc;
fn main(){ let (tx,rx)=mpsc::sync_channel(1); tx.send(1).expect("receiver"); assert_eq!(rx.recv().ok(),Some(1)); }
