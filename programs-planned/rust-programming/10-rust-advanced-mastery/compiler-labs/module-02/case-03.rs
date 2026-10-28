trait A{type X;}struct S;impl A for S{type X=u8;}fn main(){let x:<S as A>::X=1;assert_eq!(x,1);}
