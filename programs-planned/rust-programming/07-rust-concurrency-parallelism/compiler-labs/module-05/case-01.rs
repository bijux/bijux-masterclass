use std::sync::mpsc;
fn main(){ let (tx,rx)=mpsc::channel(); tx.send(String::from("x")).expect("receiver"); assert_eq!(rx.recv().ok().as_deref(),Some("x")); }
