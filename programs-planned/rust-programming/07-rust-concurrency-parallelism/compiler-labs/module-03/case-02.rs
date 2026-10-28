use std::sync::Mutex;
fn main(){ let m=Mutex::new((2u8,3u8)); let snapshot={ let g=m.lock().expect("lock"); *g }; assert_eq!(snapshot,(2,3)); }
