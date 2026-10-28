#![allow(dead_code)]
use std::net::UdpSocket;
fn consume(_: UdpSocket) {}
fn main() { let function: fn(UdpSocket) = consume; let _ = function; }
