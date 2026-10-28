#![allow(dead_code, unused_imports, unused_variables)]
struct Owner(String); impl Drop for Owner{fn drop(&mut self){}} fn take(owner:Owner)->String{owner.0} fn main(){}
