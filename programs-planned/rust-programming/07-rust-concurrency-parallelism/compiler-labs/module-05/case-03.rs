use std::sync::mpsc; use std::thread;
fn main(){ let (tx,rx)=mpsc::channel(); let tx2=tx.clone(); let h=thread::spawn(move || tx2.send(2)); tx.send(1).ok(); drop(tx); let _=h.join(); let mut v:Vec<_>=rx.iter().collect(); v.sort(); assert_eq!(v,vec![1,2]); }
