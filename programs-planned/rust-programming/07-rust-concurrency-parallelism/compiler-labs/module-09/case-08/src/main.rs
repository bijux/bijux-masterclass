use rayon::prelude::*;
fn main(){ let v=vec![1,2,3]; let _sum:i32=v.into_par_iter().sum(); println!("{}",v.len()); }
