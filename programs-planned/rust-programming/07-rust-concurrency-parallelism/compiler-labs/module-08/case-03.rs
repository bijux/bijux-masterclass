struct Marker;
unsafe impl Send for Marker {}
fn main(){ let _=Marker; }
