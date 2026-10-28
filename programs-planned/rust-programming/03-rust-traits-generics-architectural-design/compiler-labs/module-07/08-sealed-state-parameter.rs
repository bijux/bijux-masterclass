mod api{mod p{pub trait S{}pub struct D;impl S for D{}}pub trait State:p::S{}impl State for p::D{}pub struct X<T:State>(T);}fn main(){}
