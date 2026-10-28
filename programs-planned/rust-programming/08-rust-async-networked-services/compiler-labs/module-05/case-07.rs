#![allow(dead_code)]
struct Message { body: String }
fn consume(_: Message) {}
fn main() { let message = Message { body: "job".into() }; consume(message); println!("{}", message.body); }
