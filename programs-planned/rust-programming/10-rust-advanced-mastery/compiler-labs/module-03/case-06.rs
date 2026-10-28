fn apply<F>(f:F)->&'static str where F:for<'a>Fn(&'a str)->&'a str{let s=String::from("x");f(&s)}fn main(){println!("{}",apply(|x|x));}
