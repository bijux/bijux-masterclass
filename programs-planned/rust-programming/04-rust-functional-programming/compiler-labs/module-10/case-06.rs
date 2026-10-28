fn main(){
 let (ok,bad)=[Ok(1),Err("x"),Ok(2)].into_iter().fold((vec![],vec![]),|(mut ok,mut bad),item|{match item{Ok(v)=>ok.push(v),Err(e)=>bad.push(e)}(ok,bad)});
 assert_eq!(ok,vec![1,2]);assert_eq!(bad,vec!["x"]);
}
