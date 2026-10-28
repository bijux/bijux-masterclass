// outcome: fail
// lesson: Mutable storage cannot accept a shorter inner reference

fn overwrite<'a>(slot:&mut &'static str,short:&'a str){*slot=short;}fn main(){}
