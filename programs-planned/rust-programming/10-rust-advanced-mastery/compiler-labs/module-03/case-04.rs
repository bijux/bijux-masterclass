struct C(String);impl C{fn view(&mut self)->&str{&self.0}}fn main(){let mut c=C("x".into());let a=c.view();let b=c.view();println!("{a}{b}");}
