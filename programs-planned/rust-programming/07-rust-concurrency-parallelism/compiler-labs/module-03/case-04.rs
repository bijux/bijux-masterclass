use std::sync::Mutex;
fn main(){ let m=Mutex::new(1); let value=m.lock().map(|g|*g).unwrap_or_default(); assert_eq!(value,1); }
