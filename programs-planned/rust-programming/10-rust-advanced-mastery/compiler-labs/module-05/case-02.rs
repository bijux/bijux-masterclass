fn values(flag:bool)->impl Iterator<Item=u8>{if flag{0..3}else{vec![1,2].into_iter()}}fn main(){println!("{}",values(true).count());}
