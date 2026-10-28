mod m{pub struct N(String);impl N{pub fn new(s:String)->Option<Self>{(!s.is_empty()).then_some(Self(s))}}}fn main(){let _=m::N(String::new());}
