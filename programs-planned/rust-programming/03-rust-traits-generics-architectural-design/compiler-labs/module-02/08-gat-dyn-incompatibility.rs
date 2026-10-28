trait Lend{type Item<'a> where Self:'a;fn get(&self)->Self::Item<'_>;}fn use_it(_: &dyn Lend){}fn main(){}
