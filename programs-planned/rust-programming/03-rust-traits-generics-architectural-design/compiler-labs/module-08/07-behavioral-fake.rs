trait Load{fn load(self)->Result<u8,()>;}struct Fake(bool);impl Load for Fake{fn load(self)->Result<u8,()>{if self.0{Err(())}else{Ok(1)}}}fn main(){assert!(Fake(true).load().is_err());}
