#![allow(dead_code, unused_imports, unused_variables)]
fn prefix(bytes:&[u8],length:usize)->Option<&[u8]>{if length>bytes.len(){return None;}let pointer=bytes.as_ptr(); // SAFETY: `length` is in bounds and the result is tied to `bytes`.
 Some(unsafe{std::slice::from_raw_parts(pointer,length)})} fn main(){assert_eq!(prefix(b"abc",2),Some(&b"ab"[..]));}
