fn main(){
 let message=String::from("hello");
 let _task:Box<dyn Fn() + 'static>=Box::new(||println!("{message}"));
}
