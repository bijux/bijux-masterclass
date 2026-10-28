macro_rules! once {($e:expr)=>{{let v=$e;v}};}
fn main(){let mut n=0;let v=once!({n+=1;n});assert_eq!((v,n),(1,1));}
