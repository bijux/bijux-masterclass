fn values()->impl Iterator<Item=u8>{0..3}fn main(){assert_eq!(values().sum::<u8>(),3);}
