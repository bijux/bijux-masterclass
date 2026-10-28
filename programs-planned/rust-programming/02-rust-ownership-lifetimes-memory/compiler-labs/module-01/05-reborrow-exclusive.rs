// outcome: pass
// lesson: A mutable reference can be reborrowed for a shorter call

fn add(x:&mut i32){*x+=1} fn main(){let mut v=0; let r=&mut v; add(r); add(r); assert_eq!(*r,2);}
