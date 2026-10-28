fn choose(flag:bool)->impl Fn(i32)->i32{move|value|if flag{value+1}else{value*2}}
fn main(){assert_eq!(choose(false)(3),6);}
