#![allow(dead_code)]
use std::net::SocketAddr;
fn invalid<'a>() -> &'a SocketAddr { let address: SocketAddr = "127.0.0.1:80".parse().unwrap(); &address }
fn main() {}
