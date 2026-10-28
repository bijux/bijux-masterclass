fn needs_static<T: 'static>(_: T) {}
fn main(){ needs_static(String::from("owned")); }
