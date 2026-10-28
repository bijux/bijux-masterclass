fn check<F:Fn(&i32)->bool>(f:F)->bool{f(&1)&&f(&2)}
fn main(){let mut calls=0;let _=check(|_|{calls+=1;true});}
