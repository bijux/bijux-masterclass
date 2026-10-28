#![forbid(unsafe_code)]

use proc_macro::TokenStream;
use quote::quote;
use syn::ext::IdentExt;
use syn::{parse_macro_input, Data, DeriveInput, Fields, LitStr};

#[derive(Default)]
struct FieldPolicy {
    skip: bool,
    rename: Option<LitStr>,
}

fn parse_policy(field: &syn::Field) -> syn::Result<FieldPolicy> {
    let mut policy = FieldPolicy::default();

    for attribute in &field.attrs {
        if !attribute.path().is_ident("field_names") {
            continue;
        }

        attribute.parse_nested_meta(|meta| {
            if meta.path.is_ident("skip") {
                if policy.skip {
                    return Err(meta.error("duplicate `skip`"));
                }
                if policy.rename.is_some() {
                    return Err(meta.error("`skip` cannot be combined with `rename`"));
                }
                policy.skip = true;
                return Ok(());
            }

            if meta.path.is_ident("rename") {
                if policy.rename.is_some() {
                    return Err(meta.error("duplicate `rename`"));
                }
                if policy.skip {
                    return Err(meta.error("`rename` cannot be combined with `skip`"));
                }

                let value: LitStr = meta.value()?.parse()?;
                if value.value().is_empty() {
                    return Err(syn::Error::new(
                        value.span(),
                        "rename value must not be empty",
                    ));
                }
                policy.rename = Some(value);
                return Ok(());
            }

            Err(meta.error("expected `skip` or `rename = \"...\"`"))
        })?;
    }

    Ok(policy)
}

#[proc_macro_derive(FieldNames, attributes(field_names))]
pub fn derive_field_names(input: TokenStream) -> TokenStream {
    match expand(parse_macro_input!(input as DeriveInput)) {
        Ok(tokens) => tokens.into(),
        Err(error) => error.to_compile_error().into(),
    }
}

fn expand(input: DeriveInput) -> syn::Result<proc_macro2::TokenStream> {
    let ident = input.ident;
    let fields = match input.data {
        Data::Struct(data) => match data.fields {
            Fields::Named(named) => named.named,
            Fields::Unit => Default::default(),
            Fields::Unnamed(fields) => {
                return Err(syn::Error::new_spanned(
                    fields,
                    "FieldNames supports named-field or unit structs",
                ));
            }
        },
        Data::Enum(data) => {
            return Err(syn::Error::new_spanned(
                data.enum_token,
                "FieldNames does not support enums",
            ));
        }
        Data::Union(data) => {
            return Err(syn::Error::new_spanned(
                data.union_token,
                "FieldNames does not support unions",
            ));
        }
    };

    let mut names = Vec::new();
    let mut errors: Option<syn::Error> = None;

    for field in fields {
        match parse_policy(&field) {
            Ok(policy) if !policy.skip => {
                if let Some(rename) = policy.rename {
                    names.push(rename);
                } else if let Some(field_ident) = field.ident {
                    names.push(LitStr::new(
                        &field_ident.unraw().to_string(),
                        field_ident.span(),
                    ));
                }
            }
            Ok(_) => {}
            Err(error) => {
                if let Some(all) = &mut errors {
                    all.combine(error);
                } else {
                    errors = Some(error);
                }
            }
        }
    }

    if let Some(error) = errors {
        return Err(error);
    }

    let generics = input.generics;
    let (impl_generics, type_generics, where_clause) = generics.split_for_impl();

    Ok(quote! {
        impl #impl_generics #ident #type_generics #where_clause {
            pub const FIELD_NAMES: &'static [&'static str] = &[#(#names),*];
            pub const FIELD_COUNT: usize = Self::FIELD_NAMES.len();
        }
    })
}
