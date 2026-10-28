#![allow(dead_code)]
#[derive(Clone, Copy)] enum Connection { Resolving, Connecting, Open, Closing, Closed }
fn terminal(state: Connection) -> bool { match state { Connection::Closed => true, Connection::Resolving | Connection::Connecting | Connection::Open | Connection::Closing => false } }
fn main() { assert!(terminal(Connection::Closed)); }
