fn numbers(flag:bool)->impl Iterator<Item=i32>{
 if flag {0..3} else {vec![7,8].into_iter()}
}
fn main(){let _=numbers(true);}
