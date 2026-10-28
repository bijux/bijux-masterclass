fn use_twice<F:Fn()->u64>(f:F)->u64{f()+f()}
fn main(){let mut n=0;let _=use_twice(||{n+=1;n});}
