fn numbers(flag:bool)->Box<dyn Iterator<Item=i32>>{
 if flag{Box::new(0..3)}else{Box::new(vec![7,8].into_iter())}
}
fn main(){assert_eq!(numbers(false).collect::<Vec<_>>(),vec![7,8]);}
