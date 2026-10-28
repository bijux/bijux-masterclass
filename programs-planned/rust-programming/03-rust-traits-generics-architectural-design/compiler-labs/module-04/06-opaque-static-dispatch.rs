fn values()->impl Iterator<Item=u8>{[1,2,3].into_iter()}fn main(){assert_eq!(values().sum::<u8>(),6);}
