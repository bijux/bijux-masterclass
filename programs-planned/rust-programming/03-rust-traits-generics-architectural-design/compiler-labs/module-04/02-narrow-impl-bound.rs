struct Pair<T>(T,T);impl<T> Pair<T>{fn first(&self)->&T{&self.0}}impl<T:PartialOrd> Pair<T>{fn max(&self)->&T{if self.0>=self.1{&self.0}else{&self.1}}}fn main(){assert_eq!(*Pair(1,2).max(),2);}
