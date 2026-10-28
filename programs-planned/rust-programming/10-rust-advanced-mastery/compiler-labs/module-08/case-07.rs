fn walk(depth:u8,count:&mut u32){*count+=1;if depth>0{walk(depth-1,count);walk(depth-1,count)}}fn main(){let mut n=0;walk(3,&mut n);assert_eq!(n,15);}
