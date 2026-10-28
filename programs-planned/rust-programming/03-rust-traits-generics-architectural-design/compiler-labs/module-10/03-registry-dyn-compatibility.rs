trait Rule{fn run<T>(&self,t:T);}fn registry()->Vec<Box<dyn Rule>>{Vec::new()}fn main(){}
