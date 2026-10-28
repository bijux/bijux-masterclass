trait V{fn map<T>(&self,x:T)->T;}fn call(v:&dyn V){let _=v.map(1_u8);}fn main(){}
