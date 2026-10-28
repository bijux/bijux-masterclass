use std::sync::mpsc;
fn main(){ let (tx,rx)=mpsc::channel::<String>(); drop(rx); let err=tx.send(String::from("job")).expect_err("closed"); assert_eq!(err.0,"job"); }
