struct R{key:String}impl R{fn new(k:String)->Option<Self>{(!k.is_empty()).then_some(Self{key:k})}}fn main(){assert_eq!(R::new("k".into()).unwrap().key,"k");}
