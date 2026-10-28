#![forbid(unsafe_code)]

use proc_macro::TokenStream;
use quote::{format_ident, quote};
use std::collections::BTreeSet;
use syn::{
    parse::{Parse, ParseStream},
    parse_macro_input,
    punctuated::Punctuated,
    DeriveInput, Ident, ItemFn, LitStr, Result, Token,
};

#[proc_macro]
pub fn emit_answer(_input: TokenStream) -> TokenStream { quote!(42_u32).into() }

#[proc_macro]
pub fn token_count(input: TokenStream) -> TokenStream {
    let count = proc_macro2::TokenStream::from(input).into_iter().count();
    quote!(#count).into()
}

#[proc_macro_derive(TypeName)]
pub fn type_name(input: TokenStream) -> TokenStream {
    let input = parse_macro_input!(input as DeriveInput);
    let ident = input.ident;
    let generics = input.generics;
    let (impl_generics, ty_generics, where_clause) = generics.split_for_impl();
    quote! { impl #impl_generics #ident #ty_generics #where_clause { pub const TYPE_NAME: &'static str = stringify!(#ident); } }.into()
}

#[proc_macro_derive(FieldCount)]
pub fn field_count(input: TokenStream) -> TokenStream {
    let input = parse_macro_input!(input as DeriveInput);
    let ident = input.ident;
    let count = match input.data {
        syn::Data::Struct(data) => data.fields.len(),
        _ => return syn::Error::new_spanned(ident, "FieldCount supports structs only").to_compile_error().into(),
    };
    let generics=input.generics;
    let (impl_generics,ty_generics,where_clause)=generics.split_for_impl();
    quote! { impl #impl_generics #ident #ty_generics #where_clause { pub const FIELD_COUNT: usize = #count; } }.into()
}

#[proc_macro_attribute]
pub fn require_public(args: TokenStream, item: TokenStream) -> TokenStream {
    if !args.is_empty() { return syn::Error::new(proc_macro2::Span::call_site(), "require_public accepts no arguments").to_compile_error().into(); }
    let function=parse_macro_input!(item as ItemFn);
    if !matches!(&function.vis, syn::Visibility::Public(_)) {
        return syn::Error::new_spanned(&function.sig.ident, "handler function must be public").to_compile_error().into();
    }
    quote!(#function).into()
}

struct IdentList(Punctuated<Ident, Token![,]>);
impl Parse for IdentList { fn parse(input: ParseStream<'_>) -> Result<Self> { Ok(Self(Punctuated::parse_terminated(input)?)) } }

#[proc_macro]
pub fn unique_idents(input: TokenStream) -> TokenStream {
    let list=parse_macro_input!(input as IdentList);
    let mut seen=BTreeSet::new();
    let mut errors: Option<syn::Error>=None;
    for ident in &list.0 {
        let name=ident.to_string();
        if !seen.insert(name) {
            let err=syn::Error::new_spanned(ident, "duplicate identifier");
            if let Some(all)=&mut errors { all.combine(err); } else { errors=Some(err); }
        }
    }
    if let Some(err)=errors { return err.to_compile_error().into(); }
    let names = list
        .0
        .iter()
        .map(|identifier| LitStr::new(&identifier.to_string(), identifier.span()));
    quote!(&[#(#names),*]).into()
}

#[proc_macro_attribute]
pub fn metadata(args: TokenStream, item: TokenStream) -> TokenStream {
    let name=parse_macro_input!(args as Ident);
    let function=parse_macro_input!(item as ItemFn);
    let const_name=format_ident!("{}_METADATA", name.to_string().to_uppercase());
    let fn_name=&function.sig.ident;
    quote! { #function pub const #const_name: (&str, fn() -> u32) = (stringify!(#fn_name), #fn_name); }.into()
}
