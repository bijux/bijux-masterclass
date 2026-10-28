fn main(){let s=String::from("x");let owned=(&s[..]).to_owned();drop(s);assert_eq!(owned,"x");}
