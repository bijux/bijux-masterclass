use std::thread;
fn main(){ let mut v=[1,2,3]; thread::scope(|s| { let a=&mut v[..2]; let b=&mut v[1..]; s.spawn(move || a[0]+=1); s.spawn(move || b[0]+=1); }); }
