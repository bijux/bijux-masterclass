trait S{type E;fn load(&self)->Result<u8,Self::E>;}fn use_it(_:Box<dyn S>){}fn main(){}
