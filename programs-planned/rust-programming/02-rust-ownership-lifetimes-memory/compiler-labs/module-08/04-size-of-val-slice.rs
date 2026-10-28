// outcome: pass
// lesson: size_of_val uses slice metadata

fn main(){let s:&[u16]=&[1,2,3];assert_eq!(std::mem::size_of_val(s),6);}
