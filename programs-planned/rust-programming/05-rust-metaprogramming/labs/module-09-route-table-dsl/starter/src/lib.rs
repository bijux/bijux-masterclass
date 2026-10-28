#![forbid(unsafe_code)]

use proc_macro::{Literal, TokenStream};

#[proc_macro]
pub fn route_table(_input: TokenStream) -> TokenStream {
    let value = Literal::usize_unsuffixed(0);
    let declaration = format!("const ROUTE_COUNT: usize = {value};");
    declaration
        .parse()
        .expect("the fixed baseline declaration must parse")
}
