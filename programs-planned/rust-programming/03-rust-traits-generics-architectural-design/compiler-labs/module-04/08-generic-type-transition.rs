struct P<A,B>(A,B);impl<A,B>P<A,B>{fn map<C>(self,c:C)->P<A,C>{P(self.0,c)}}fn main(){let _:P<u8,&str>=P(1,2u8).map("x");}
