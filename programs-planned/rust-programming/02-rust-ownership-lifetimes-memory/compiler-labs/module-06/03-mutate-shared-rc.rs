// outcome: fail
// lesson: Shared Rc access cannot mutate ordinary T

use std::rc::Rc;fn main(){let value=Rc::new(String::from("x"));value.push('!');}
