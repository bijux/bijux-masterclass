use std::fmt::Display;fn show(a:impl Display,b:impl Display)->String{format!("{a}{b}")}fn main(){assert_eq!(show(1,"x"),"1x");}
