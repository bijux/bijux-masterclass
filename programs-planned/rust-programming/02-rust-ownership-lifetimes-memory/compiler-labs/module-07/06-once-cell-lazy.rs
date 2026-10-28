// outcome: pass
// lesson: OnceCell initializes through shared access

use std::cell::OnceCell;fn main(){let c=OnceCell::new();assert_eq!(*c.get_or_init(||3),3);}
