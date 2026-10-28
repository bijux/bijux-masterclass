use std::{env,fs,path::PathBuf};fn main(){let out=PathBuf::from(env::var("OUT_DIR").unwrap());fs::write(out.join("generated.rs"),"pub const VALUE:u32=1;\n").unwrap();}
