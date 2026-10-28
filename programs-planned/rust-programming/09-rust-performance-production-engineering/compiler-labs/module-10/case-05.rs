fn owner<'a>() -> &'a str { let local=String::from("on-call"); &local } fn main(){println!("{}",owner());}
