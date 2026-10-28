// outcome: pass
// lesson: Ordinary Box does not prohibit moving its pointee out

fn main(){let b=Box::new(String::from("x"));let s:String=*b;assert_eq!(s,"x");}
