#![forbid(unsafe_code)]

use proc_macro::TokenStream;
use quote::quote;
use syn::{parse_macro_input, DeriveInput};

#[proc_macro_derive(FieldNames, attributes(field_names))]
pub fn derive_field_names(input: TokenStream) -> TokenStream {
    let input = parse_macro_input!(input as DeriveInput);
    let ident = input.ident;
    let generics = input.generics;
    let (impl_generics, type_generics, where_clause) = generics.split_for_impl();

    quote! {
        impl #impl_generics #ident #type_generics #where_clause {
            pub const FIELD_NAMES: &'static [&'static str] = &[];
        }
    }
    .into()
}
