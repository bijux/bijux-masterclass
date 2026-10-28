#![allow(dead_code)]
use std::net::SocketAddr;
fn main() { let address: SocketAddr = "127.0.0.1:8080".parse().unwrap(); assert_eq!(address.port(), 8080); }
