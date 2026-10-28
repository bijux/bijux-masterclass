trait Convert<T>{fn convert(&self)->T;}struct Bytes(Vec<u8>);
impl Convert<Vec<u8>> for Bytes{fn convert(&self)->Vec<u8>{self.0.clone()}}
impl Convert<String> for Bytes{fn convert(&self)->String{String::from_utf8_lossy(&self.0).into_owned()}}
fn main(){let b=Bytes(vec![97]);let _:String=b.convert();let _:Vec<u8>=b.convert();}
