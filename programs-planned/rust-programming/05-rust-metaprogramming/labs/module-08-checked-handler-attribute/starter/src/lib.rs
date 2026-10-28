#![forbid(unsafe_code)]

use proc_macro::TokenStream;
use quote::quote;
use syn::{parse_macro_input, ItemFn};

#[proc_macro_attribute]
pub fn checked_handler(
    _arguments: TokenStream,
    item: TokenStream,
) -> TokenStream {
    let function = parse_macro_input!(item as ItemFn);
    quote!(#function).into()
}
