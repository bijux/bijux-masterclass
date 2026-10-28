mod api{pub struct Reviewed(());pub struct Doc<S>{state:S}impl Doc<Reviewed>{pub fn publish(self){}}}fn main(){let _=api::Reviewed(());}
