mod m{pub struct Percent(u8);impl Percent{pub fn new(v:u8)->Option<Self>{(v<=100).then_some(Self(v))}pub fn get(&self)->u8{self.0}}}fn main(){assert_eq!(m::Percent::new(50).unwrap().get(),50);}
