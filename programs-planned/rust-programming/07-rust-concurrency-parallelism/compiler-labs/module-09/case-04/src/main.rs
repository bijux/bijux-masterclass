use rayon::prelude::*; use rayon::ThreadPoolBuilder;
fn main(){ let pool=ThreadPoolBuilder::new().num_threads(2).build().expect("pool"); let n=pool.install(||(0..10).into_par_iter().sum::<i32>()); assert_eq!(n,45); }
