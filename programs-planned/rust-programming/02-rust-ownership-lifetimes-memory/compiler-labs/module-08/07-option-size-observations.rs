// outcome: pass
// lesson: Option sizes can reveal documented and undocumented niches

fn main(){println!("{} {}",std::mem::size_of::<&u8>(),std::mem::size_of::<Option<&u8>>());}
