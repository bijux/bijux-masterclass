trait T{fn f(&self);}fn call<X:T>(x:&X){x.f()}fn main(){let _p:fn(&dyn T)=call::<dyn T>;}
