// outcome: pass
// lesson: The compiler permits but design review rejects panicking Drop
struct Bad;
impl Drop for Bad{
    fn drop(&mut self){
        if std::thread::panicking(){
            return;
        }
        /* still poor policy */
    }
}
fn main(){
    let _b=Bad;
}
