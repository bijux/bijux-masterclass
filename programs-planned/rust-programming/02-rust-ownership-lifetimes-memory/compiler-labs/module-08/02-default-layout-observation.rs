// outcome: pass
// lesson: Default field addresses are observations only

struct H{a:u8,b:u32,c:u16}fn main(){let h=H{a:1,b:2,c:3};println!("{:p} {:p} {:p}",&h.a,&h.b,&h.c);}
