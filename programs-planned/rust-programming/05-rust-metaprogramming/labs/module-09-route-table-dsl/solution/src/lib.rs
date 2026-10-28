#![forbid(unsafe_code)]

use proc_macro::TokenStream;
use quote::quote;
use std::collections::BTreeMap;
use syn::parse::{Parse, ParseStream};
use syn::{
    braced, parse_macro_input, Ident, LitStr, Path, Result, Token, Visibility,
};

struct RouteEntry {
    method: Ident,
    path: LitStr,
    handler: Path,
}

struct RouteInput {
    visibility: Visibility,
    name: Ident,
    entries: Vec<RouteEntry>,
}

impl Parse for RouteInput {
    fn parse(input: ParseStream<'_>) -> Result<Self> {
        let visibility = input.parse()?;
        input.parse::<Token![static]>()?;
        let name = input.parse()?;

        let content;
        braced!(content in input);
        let mut entries = Vec::new();

        while !content.is_empty() {
            let method = content.parse()?;
            let path = content.parse()?;
            content.parse::<Token![=>]>()?;
            let handler = content.parse()?;
            content.parse::<Token![;]>()?;
            entries.push(RouteEntry {
                method,
                path,
                handler,
            });
        }

        Ok(Self {
            visibility,
            name,
            entries,
        })
    }
}

#[proc_macro]
pub fn route_table(input: TokenStream) -> TokenStream {
    let input = parse_macro_input!(input as RouteInput);
    match expand(input) {
        Ok(tokens) => tokens.into(),
        Err(error) => error.to_compile_error().into(),
    }
}

fn expand(input: RouteInput) -> Result<proc_macro2::TokenStream> {
    let mut seen: BTreeMap<(String, String), proc_macro2::Span> = BTreeMap::new();

    for entry in &input.entries {
        let method = entry.method.to_string();
        if !matches!(method.as_str(), "GET" | "POST" | "PUT" | "DELETE") {
            return Err(syn::Error::new(
                entry.method.span(),
                "supported methods are GET, POST, PUT, DELETE",
            ));
        }

        let path = entry.path.value();
        if !path.starts_with('/') {
            return Err(syn::Error::new(
                entry.path.span(),
                "route path must start with `/`",
            ));
        }

        let key = (method, path);
        if let Some(first_span) = seen.get(&key).copied() {
            let mut error = syn::Error::new(
                entry.method.span(),
                "duplicate method/path route",
            );
            error.combine(syn::Error::new(first_span, "first declared here"));
            return Err(error);
        }
        seen.insert(key, entry.method.span());
    }

    let visibility = input.visibility;
    let table_name = input.name;
    let rows = input.entries.iter().map(|entry| {
        let method = Ident::new(
            &method_variant(&entry.method.to_string()),
            entry.method.span(),
        );
        let path = &entry.path;
        let handler = &entry.handler;
        quote! {
            Route {
                method: Method::#method,
                path: #path,
                handler: #handler,
            }
        }
    });

    Ok(quote! {
        #[derive(Debug, Clone, Copy, PartialEq, Eq)]
        #visibility enum Method {
            Get,
            Post,
            Put,
            Delete,
        }

        #[derive(Clone, Copy)]
        #visibility struct Route {
            pub method: Method,
            pub path: &'static str,
            pub handler: fn(&str) -> ::std::string::String,
        }

        #visibility static #table_name: &[Route] = &[#(#rows),*];

        #visibility fn dispatch(
            method: Method,
            path: &str,
            input: &str,
        ) -> ::std::option::Option<::std::string::String> {
            #table_name
                .iter()
                .find(|route| route.method == method && route.path == path)
                .map(|route| (route.handler)(input))
        }
    })
}

fn method_variant(method: &str) -> String {
    let mut characters = method.chars();
    match characters.next() {
        Some(first) => first
            .to_uppercase()
            .chain(characters.flat_map(char::to_lowercase))
            .collect(),
        None => String::new(),
    }
}
