mod library { mod support { fn hidden()->u32{1} } #[macro_export] macro_rules! hidden_value {()=>{$crate::library::support::hidden()};} }
mod consumer { pub fn run()->u32 { crate::hidden_value!() } }
fn main(){let _=consumer::run();}
