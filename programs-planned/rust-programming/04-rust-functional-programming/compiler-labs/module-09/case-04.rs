#[derive(Debug)]struct FieldError<E>{field:&'static str,source:E}
fn context<T,E,F:FnOnce()->Result<T,E>>(field:&'static str,f:F)->Result<T,FieldError<E>>{f().map_err(|source|FieldError{field,source})}
fn main(){assert_eq!(context("n",||"x".parse::<u8>()).unwrap_err().field,"n");}
