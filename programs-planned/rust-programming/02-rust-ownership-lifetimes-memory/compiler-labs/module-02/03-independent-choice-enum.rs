// outcome: pass
// lesson: An enum can preserve independent source lifetimes
enum Choice<'a,'b>{
    A(&'a str),B(&'b str)
}
fn choose<'a,'b>(a:&'a str,b:&'b str,f:bool)->Choice<'a,'b>{
    if f{
        Choice::A(a)
    }
    else{
        Choice::B(b)
    }
}
fn main(){
    let a=String::from("a");
    {
        let b=String::from("b");
        match choose(&a,&b,false){
            Choice::B(v)=>assert_eq!(v,"b"),Choice::A(_)=>{
            }
        }
    }
}
