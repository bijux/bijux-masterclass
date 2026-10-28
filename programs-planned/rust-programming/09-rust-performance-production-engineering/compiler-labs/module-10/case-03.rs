fn headroom(capacity:u64,planned:u64)->Option<u64>{capacity.checked_sub(planned)} fn main(){assert_eq!(headroom(100,80),Some(20));}
