fn visit<F>(f:F)where F:for<'a>Fn(&'a str){let a=String::from("a");f(&a);let b=String::from("b");f(&b);}fn main(){visit(|x|assert_eq!(x.len(),1));}
