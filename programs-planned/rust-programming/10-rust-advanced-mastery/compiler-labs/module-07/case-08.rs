fn choose(flag:bool)->impl Fn(u8)->u8{let add=1_u8;let multiply=2_u8;if flag{move|x|x+add}else{move|x|x*multiply}}fn main(){println!("{}",choose(true)(3));}
