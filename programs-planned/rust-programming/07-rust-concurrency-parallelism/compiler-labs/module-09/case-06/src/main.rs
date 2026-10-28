use rayon::prelude::*; use std::rc::Rc;
fn main(){ let n=Rc::new(1); let _v:Vec<_>=(0..4).into_par_iter().map(|x|x+*n).collect(); }
