struct D{value:String}impl Drop for D{fn drop(&mut self){}}fn main(){let d=D{value:"x".into()};let _v=d.value;}
