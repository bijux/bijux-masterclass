trait Meta{const NAME:&'static str;fn run(&self){}}fn use_it(_: &dyn Meta){}fn main(){}
