// outcome: fail
// lesson: A partially moved struct cannot be used as a whole

#[derive(Debug)] struct Record { title:String, score:u8 }
fn main(){ let r=Record{title:"x".into(),score:1}; let _title=r.title; println!("{r:?}"); }
