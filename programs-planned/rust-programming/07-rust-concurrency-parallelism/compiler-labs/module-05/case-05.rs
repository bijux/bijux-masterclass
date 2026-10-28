use std::sync::mpsc;
fn main(){ let (_tx,rx)=mpsc::channel::<u8>(); let _=rx.clone(); }
