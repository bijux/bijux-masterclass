#![allow(dead_code, unused_imports, unused_variables)]
fn first(bytes:&[u8])->Option<u8>{let pointer=bytes.first()? as *const u8; // SAFETY: pointer originates from the live first element.
 Some(unsafe{*pointer})} fn main(){assert_eq!(first(b"x"),Some(b'x'));}
