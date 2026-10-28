trait A{fn value(&self)->u8;}struct S;impl A for S{fn value(&self)->u8{1}}fn main(){assert_eq!(A::value(&S),1);}
