#![forbid(unsafe_code)]

use proc_macro::{Literal, TokenStream, TokenTree};

#[proc_macro]
pub fn token_tree_shape(_input: TokenStream) -> TokenStream {
    TokenStream::from(TokenTree::Literal(Literal::string("uninspected")))
}
