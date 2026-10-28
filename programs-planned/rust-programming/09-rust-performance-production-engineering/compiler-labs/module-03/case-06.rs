use std::rc::Rc; use std::thread; fn main() { let data = Rc::new(vec![1]); thread::spawn(move || println!("{}", data.len())); }
