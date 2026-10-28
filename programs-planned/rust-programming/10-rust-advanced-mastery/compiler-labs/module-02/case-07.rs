trait P{type O;}fn copy<T:P>(x:&T::O)->T::O where T::O:Clone{x.clone()}struct S;impl P for S{type O=String;}fn main(){let value=String::from("x");assert_eq!(copy::<S>(&value),"x");}
