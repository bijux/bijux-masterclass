#![allow(dead_code, unused_imports, unused_variables)]
enum Error{Parse,Path} fn classify(parse:bool)->Result<(),Error>{if !parse{return Err(Error::Parse)};Ok(())} fn main(){assert!(classify(false).is_err());}
