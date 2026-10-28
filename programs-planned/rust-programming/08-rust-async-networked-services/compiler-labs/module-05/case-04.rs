#![allow(dead_code)]
#[derive(Debug)] enum Message { Request { id: u64, body: String }, Close }
fn handle(message: Message) -> usize { match message { Message::Request { body, .. } => body.len(), Message::Close => 0 } }
fn main() { assert_eq!(handle(Message::Request { id: 1, body: "work".into() }), 4); }
