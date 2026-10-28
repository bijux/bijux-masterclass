struct M;struct P<T>(T);struct B<S,POL>(S,POL);impl B<M,M>{fn new()->Self{B(M,M)}}impl<S> B<P<S>,P<u8>>{fn build(self){}}fn main(){let _=B::new().build();}
