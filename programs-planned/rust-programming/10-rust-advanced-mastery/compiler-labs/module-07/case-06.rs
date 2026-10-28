trait P{type O;fn out(&self)->Self::O;}fn main(){let _x:Option<Box<dyn P>>=None;}
