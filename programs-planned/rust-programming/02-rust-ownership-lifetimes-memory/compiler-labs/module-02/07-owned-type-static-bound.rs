// outcome: pass
// lesson: T: static does not require the local owner to live forever

fn accepts<T:'static>(_:T){} fn main(){let local=String::from("owned"); accepts(local);}
