trait Words{fn words(&self)->usize;}impl Words for str{fn words(&self)->usize{self.split_whitespace().count()}}fn main(){assert_eq!("a b".words(),2);}
