mod api{mod p{pub trait S{}}pub trait T:p::S{fn x(&self)->u8;}pub struct X;impl p::S for X{}impl T for X{fn x(&self)->u8{1}}}use api::T;fn main(){assert_eq!(api::X.x(),1);}
