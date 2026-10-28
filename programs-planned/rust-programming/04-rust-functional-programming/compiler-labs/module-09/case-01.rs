fn both<T,P:Fn(&T)->bool,Q:Fn(&T)->bool>(p:P,q:Q)->impl Fn(&T)->bool{move|v|p(v)&&q(v)}
fn main(){let positive=both(|v:&i32|*v>0,|v:&i32|*v<10);assert!(positive(&3));}
