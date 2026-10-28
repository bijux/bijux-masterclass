#![allow(dead_code, unused_imports, unused_variables)]
struct Session{count:usize} fn main(){let pointer=Box::into_raw(Box::new(Session{count:1})); // SAFETY: reconstruct exactly once from the pointer returned by Box::into_raw.
 let session=unsafe{Box::from_raw(pointer)};assert_eq!(session.count,1);}
