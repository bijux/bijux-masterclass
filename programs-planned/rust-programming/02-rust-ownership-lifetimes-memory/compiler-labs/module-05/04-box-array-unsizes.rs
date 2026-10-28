// outcome: pass
// lesson: A boxed array can coerce to boxed slice

fn main(){let a:Box<[u8;3]>=Box::new([1,2,3]);let s:Box<[u8]>=a;assert_eq!(&*s,&[1,2,3]);}
