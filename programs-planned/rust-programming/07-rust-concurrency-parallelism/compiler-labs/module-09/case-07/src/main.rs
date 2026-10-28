use rayon::prelude::*; use std::collections::BTreeMap;
fn main(){ let _=(0..4).into_par_iter().reduce(BTreeMap::new,|a,b|a+b); }
