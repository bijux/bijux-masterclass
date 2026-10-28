trait S{type O;}struct A;impl S for A{type O=u8;}fn need<T:S<O=u16>>(_:T){}fn main(){need(A);}
