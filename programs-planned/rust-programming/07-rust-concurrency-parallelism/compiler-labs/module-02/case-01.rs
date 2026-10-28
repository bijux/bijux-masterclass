use std::thread;
fn main(){ let values=vec![1,2,3]; let total=thread::scope(|s| s.spawn(|| values.iter().sum::<i32>()).join().unwrap_or(0)); assert_eq!(total,6); }
