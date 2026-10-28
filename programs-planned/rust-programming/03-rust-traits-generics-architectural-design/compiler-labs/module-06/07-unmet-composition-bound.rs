trait R{fn r(&self);}struct D<T>(T);impl<T:R>R for D<T>{fn r(&self){self.0.r()}}struct X;fn main(){D(X).r();}
