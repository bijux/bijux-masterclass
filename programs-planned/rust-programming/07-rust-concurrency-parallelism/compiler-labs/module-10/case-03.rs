enum Outcome{Done,Failed,Cancelled}
fn main(){ let values=[Outcome::Done,Outcome::Failed,Outcome::Cancelled]; assert_eq!(values.len(),3); }
