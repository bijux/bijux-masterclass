trait Encode{fn encode<T:std::fmt::Display>(&self,value:T)->String;}fn use_it(_: &dyn Encode){}fn main(){}
