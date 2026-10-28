fn due<F:FnOnce()->u64>(deadline:u64,now:F)->bool{now()>=deadline}
fn main(){assert!(due(10,||10));}
