fn main(){let mut s=String::from("a");{let r=&s;assert_eq!(r,"a");}s.push('b');{let r=&s;assert_eq!(r,"ab");}}
