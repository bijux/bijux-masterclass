mod api{mod private{pub trait Sealed{}}pub trait Token:private::Sealed{}pub struct Word;impl private::Sealed for Word{}impl Token for Word{}}
struct Mine;impl api::Token for Mine{}fn main(){}
