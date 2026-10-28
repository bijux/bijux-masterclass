trait P{type Item;fn get(&self)->Self::Item;}fn use_p(_: &dyn P){}fn main(){}
