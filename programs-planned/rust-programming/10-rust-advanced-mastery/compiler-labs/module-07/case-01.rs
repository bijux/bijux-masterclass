trait S{fn f(&self,x:u8)->u8;}struct A;impl S for A{fn f(&self,x:u8)->u8{x+1}}fn a<T:S>(s:&T)->u8{s.f(1)}fn b(s:&dyn S)->u8{s.f(1)}fn main(){assert_eq!(a(&A),b(&A));}
