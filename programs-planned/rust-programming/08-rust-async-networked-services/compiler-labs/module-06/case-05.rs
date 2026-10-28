#![allow(dead_code)]
use std::sync::mpsc::sync_channel;
fn main() { let (sender, _receiver) = sync_channel(1); let job = String::from("job"); sender.send(job).unwrap(); println!("{job}"); }
