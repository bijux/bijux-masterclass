// outcome: pass
// lesson: Safe leaks can skip cleanup
struct G<'a>(&'a mut bool);
impl Drop for G<'_>{
    fn drop(&mut self){
        *self.0=false;
    }
}
fn main(){
    let mut flag=true;
    let g=G(&mut flag);
    std::mem::forget(g);
}
