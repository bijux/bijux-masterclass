#![allow(dead_code)]
use std::net::TcpStream;
fn duplicate(stream: TcpStream) { let _other = stream.clone(); }
fn main() {}
