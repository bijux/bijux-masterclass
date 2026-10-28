trait V{fn value(&self)->&str;}struct B<'a>(&'a str);impl V for B<'_>{fn value(&self)->&str{self.0}}fn make<'a>(s:&'a str)->Box<dyn V>{Box::new(B(s))}fn main(){}
