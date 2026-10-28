mod ext{pub trait X{fn x(&self)->u8;}impl X for str{fn x(&self)->u8{1}}}fn main(){let _="a".x();}
