fn matching<'a>(xs:&'a[i32])->impl Iterator<Item=&'a i32>{xs.iter().filter(|x|**x>0)}
fn main(){let xs=[-1,2];assert_eq!(matching(&xs).copied().collect::<Vec<_>>(),vec![2]);}
