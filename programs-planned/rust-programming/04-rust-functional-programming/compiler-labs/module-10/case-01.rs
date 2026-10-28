fn main(){
 let parsed:Result<Vec<i32>,_>=["1","2","3"].into_iter().map(str::parse).collect();
 let total=parsed.unwrap().into_iter().fold(0,|sum,value|sum+value);
 assert_eq!(total,6);
}
