trait A{fn a(&self)->u8;}trait B{fn b(&self)->u8;}fn sum<T:A+B>(x:&T)->u8{x.a()+x.b()}struct X;impl A for X{fn a(&self)->u8{1}}impl B for X{fn b(&self)->u8{2}}fn main(){assert_eq!(sum(&X),3);}
