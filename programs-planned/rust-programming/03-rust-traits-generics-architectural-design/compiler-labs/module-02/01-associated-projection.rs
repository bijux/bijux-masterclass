trait Source{type Item;fn get(self)->Self::Item;} struct S;impl Source for S{type Item=u8;fn get(self)->u8{3}}
fn first<T:Source>(s:T)->T::Item{s.get()} fn main(){assert_eq!(first(S),3);}
