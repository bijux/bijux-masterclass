#![allow(dead_code, unused_imports, unused_variables)]
struct Error; fn read()->Result<Vec<u8>,Error>{Ok(std::fs::read("missing")?)} fn main(){}
