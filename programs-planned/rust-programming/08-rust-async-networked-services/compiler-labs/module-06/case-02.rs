#![allow(dead_code)]
use std::sync::mpsc::sync_channel;
fn main() { let (sender, receiver) = sync_channel(1); sender.send(String::from("owned")).unwrap(); assert_eq!(receiver.recv().unwrap(), "owned"); }
