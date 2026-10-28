use rayon::prelude::*;
fn main(){ let mut out=Vec::new(); (0..8).into_par_iter().for_each(|n|out.push(n)); }
