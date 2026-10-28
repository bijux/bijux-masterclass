use rayon::prelude::*;
fn main(){ let mut v=vec![1i32,2,3]; v.par_iter_mut().for_each(|n|*n*=2); assert_eq!(v,vec![2,4,6]); }
