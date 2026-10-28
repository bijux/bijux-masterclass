trait A{type Item;} trait B{type Item;} struct X;impl A for X{type Item=u8;}impl B for X{type Item=u16;}
fn main(){let _:X::Item=1;}
