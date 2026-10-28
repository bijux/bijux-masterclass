struct M;struct P<T>(T);struct B<S,R>(S,R);impl B<M,M>{fn new()->Self{B(M,M)}}impl<S> B<P<S>,P<u8>>{fn build(self){}}fn main(){B::new().build();}
