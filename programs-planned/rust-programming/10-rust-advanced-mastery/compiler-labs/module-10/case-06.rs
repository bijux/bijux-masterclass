struct B<const N:usize>;fn use_four(_:B<4>){}fn main(){use_four(B::<8>);}
