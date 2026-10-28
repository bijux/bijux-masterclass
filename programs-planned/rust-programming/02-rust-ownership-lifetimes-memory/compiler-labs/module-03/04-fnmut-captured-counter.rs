// outcome: pass
// lesson: A mutating capture satisfies FnMut

fn twice(mut f:impl FnMut()){f();f();} fn main(){let mut n=0; twice(||n+=1); assert_eq!(n,2);}
