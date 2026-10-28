use rayon::prelude::*;
fn main(){ let out:Vec<_>=(0..8).into_par_iter().map(|n|n*n).collect(); assert_eq!(out[3],9); }
