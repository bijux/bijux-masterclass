use std::thread;
struct Producer;
fn main(){ let p=Producer; let _a=thread::spawn(move || {let _=p;}); let _b=thread::spawn(move || {let _=p;}); }
