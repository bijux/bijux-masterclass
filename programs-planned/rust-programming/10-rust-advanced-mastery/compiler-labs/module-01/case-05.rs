fn main(){let mut s=String::from("a");let r=&s;assert_eq!(r,"a");s.push('b');assert_eq!(s,"ab");}
