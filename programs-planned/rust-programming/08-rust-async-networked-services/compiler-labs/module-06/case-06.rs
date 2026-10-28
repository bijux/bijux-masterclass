#![allow(dead_code)]
use std::sync::mpsc::{sync_channel, Receiver};
fn require_sync<T: Sync>(_: &T) {}
fn main() { let (_sender, receiver): (_, Receiver<u8>) = sync_channel(1); require_sync(&receiver); }
