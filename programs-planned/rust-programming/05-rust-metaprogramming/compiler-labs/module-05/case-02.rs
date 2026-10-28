macro_rules! diagnostic {($name:ident=$code:literal=>$msg:literal)=>{()};($name:ident=>$msg:literal)=>{compile_error!("diagnostic code is required")};}
fn main(){diagnostic!(Missing=>"missing");}
