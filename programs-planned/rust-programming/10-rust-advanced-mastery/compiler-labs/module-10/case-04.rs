fn main(){let mut s=String::from("old");let view=&s[..];s=String::from("new");println!("{view} {s}");}
