use std::thread;
fn main(){ let mut values=[-1i32,-2,-3,-4]; thread::scope(|s| { for chunk in values.chunks_mut(2){ s.spawn(move || { for v in chunk {*v=v.abs();} }); } }); assert_eq!(values,[1,2,3,4]); }
