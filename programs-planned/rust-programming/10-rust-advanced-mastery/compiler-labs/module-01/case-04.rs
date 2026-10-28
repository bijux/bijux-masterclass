trait A{fn f(&self);}trait B{fn f(&self);}struct S;impl A for S{fn f(&self){}}impl B for S{fn f(&self){}}fn main(){S.f();}
