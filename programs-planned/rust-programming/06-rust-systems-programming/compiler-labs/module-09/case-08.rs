#![allow(dead_code, unused_imports, unused_variables)]
struct Session{value:String} fn open_view()->&'static str{let session=Session{value:String::from("x")};&session.value} fn main(){}
