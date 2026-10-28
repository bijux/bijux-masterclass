// outcome: fail
// lesson: Two indexing operations do not prove disjointness

fn main() { let mut values=[1,2]; let a=&mut values[0]; let b=&mut values[1]; *a += *b; }
