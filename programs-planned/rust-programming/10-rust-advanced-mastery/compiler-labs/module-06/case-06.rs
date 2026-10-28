use std::rc::Rc;fn main(){let x=Rc::new(1);std::thread::spawn(move||println!("{x}"));}
