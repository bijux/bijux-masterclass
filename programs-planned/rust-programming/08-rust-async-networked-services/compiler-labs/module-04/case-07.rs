#![allow(dead_code)]
enum Connection { Resolving, Connecting, Open, Closing, Closed }
fn label(state: Connection) -> &'static str { match state { Connection::Resolving => "resolving", Connection::Open => "open", Connection::Closed => "closed" } }
fn main() {}
