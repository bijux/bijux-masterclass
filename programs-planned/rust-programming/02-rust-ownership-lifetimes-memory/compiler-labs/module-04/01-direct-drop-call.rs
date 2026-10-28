// outcome: fail
// lesson: Drop::drop cannot be called directly

struct G; impl Drop for G{fn drop(&mut self){}} fn main(){let mut g=G; Drop::drop(&mut g);}
