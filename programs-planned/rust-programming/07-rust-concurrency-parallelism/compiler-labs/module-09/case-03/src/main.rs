use rayon::prelude::*;
fn main(){ let total=(0usize..1000).into_par_iter().fold(||0usize,|a,n|a+n).reduce(||0,|a,b|a+b); assert_eq!(total,499500); }
