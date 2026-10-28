struct Review(Vec<u8>);impl Review{fn errors(&self)->impl Iterator<Item=&u8>{self.0.iter().filter(|x|**x>0)}}fn main(){assert_eq!(Review(vec![0,1]).errors().count(),1);}
