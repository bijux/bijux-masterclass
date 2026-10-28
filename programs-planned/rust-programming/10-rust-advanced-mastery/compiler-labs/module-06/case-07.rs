fn main(){let mut v:Vec<u8>=Vec::with_capacity(4);v.push(1);assert_eq!(v.len(),1);assert!(v.capacity()>=4);}
