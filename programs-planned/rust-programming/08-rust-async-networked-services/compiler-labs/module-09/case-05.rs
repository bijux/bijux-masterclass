#![allow(dead_code)]
fn attempt(_: String) {}
fn main() { let key = String::from("same"); attempt(key); attempt(key); }
