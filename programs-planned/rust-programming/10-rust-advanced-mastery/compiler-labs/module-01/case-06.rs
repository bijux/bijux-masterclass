fn bad<'a>()->&'a str{let s=String::from("x");&s}fn main(){println!("{}",bad());}
