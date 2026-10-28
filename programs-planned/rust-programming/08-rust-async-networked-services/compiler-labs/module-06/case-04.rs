#![allow(dead_code)]
use std::sync::mpsc::{sync_channel, SyncSender};
fn clone_sender<T>(sender: &SyncSender<T>) -> SyncSender<T> { sender.clone() }
fn main() { let (sender, _receiver) = sync_channel::<u8>(2); let other = clone_sender(&sender); drop((sender, other)); }
