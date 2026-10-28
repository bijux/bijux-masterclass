trait Source{type Item;fn get(&self)->Self::Item;}fn use_it(_: &dyn Source){}fn main(){}
