#![allow(dead_code, unused_imports, unused_variables)]
#[repr(C)] #[derive(Default)] struct Report{status:i32,offset:usize} fn main(){let report=Report::default();assert_eq!(report.status,0);}
