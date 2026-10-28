#![forbid(unsafe_code)]

use proc_macro::TokenStream;
use quote::{format_ident, quote};
use syn::parse::{Parse, ParseStream};
use syn::punctuated::Punctuated;
use syn::{
    parse_macro_input, FnArg, ItemFn, LitStr, MetaNameValue, ReturnType, Token, Type,
    Visibility,
};

struct HandlerArguments {
    items: Punctuated<MetaNameValue, Token![,]>,
}

impl Parse for HandlerArguments {
    fn parse(input: ParseStream<'_>) -> syn::Result<Self> {
        Ok(Self {
            items: Punctuated::parse_terminated(input)?,
        })
    }
}

fn parse_arguments(arguments: HandlerArguments) -> syn::Result<(LitStr, LitStr)> {
    let mut name = None;
    let mut about = None;

    for item in arguments.items {
        let Some(identifier) = item.path.get_ident() else {
            return Err(syn::Error::new_spanned(
                item.path,
                "expected `name` or `about`",
            ));
        };

        let expression = match item.value {
            syn::Expr::Lit(expression) => expression,
            other => {
                return Err(syn::Error::new_spanned(
                    other,
                    "expected a string literal",
                ));
            }
        };
        let value = match expression.lit {
            syn::Lit::Str(value) => value,
            other => {
                return Err(syn::Error::new_spanned(
                    other,
                    "expected a string literal",
                ));
            }
        };

        if value.value().is_empty() {
            return Err(syn::Error::new(
                value.span(),
                "metadata value must not be empty",
            ));
        }

        match identifier.to_string().as_str() {
            "name" => {
                if name.replace(value).is_some() {
                    return Err(syn::Error::new(identifier.span(), "duplicate `name`"));
                }
            }
            "about" => {
                if about.replace(value).is_some() {
                    return Err(syn::Error::new(identifier.span(), "duplicate `about`"));
                }
            }
            _ => {
                return Err(syn::Error::new(
                    identifier.span(),
                    "expected `name` or `about`",
                ));
            }
        }
    }

    let name = name.ok_or_else(|| {
        syn::Error::new(proc_macro2::Span::call_site(), "missing `name`")
    })?;
    let about = about.ok_or_else(|| {
        syn::Error::new(proc_macro2::Span::call_site(), "missing `about`")
    })?;

    Ok((name, about))
}

fn is_shared_str_reference(ty: &Type) -> bool {
    matches!(
        ty,
        Type::Reference(reference)
            if reference.mutability.is_none()
                && matches!(
                    reference.elem.as_ref(),
                    Type::Path(path)
                        if path.qself.is_none() && path.path.is_ident("str")
                )
    )
}

fn returns_result(output: &ReturnType) -> bool {
    matches!(
        output,
        ReturnType::Type(_, ty)
            if matches!(
                ty.as_ref(),
                Type::Path(path)
                    if path.path.segments.last().is_some_and(|segment| segment.ident == "Result")
            )
    )
}

#[proc_macro_attribute]
pub fn checked_handler(arguments: TokenStream, item: TokenStream) -> TokenStream {
    let arguments = parse_macro_input!(arguments as HandlerArguments);
    let function = parse_macro_input!(item as ItemFn);

    match expand(arguments, function) {
        Ok(tokens) => tokens.into(),
        Err(error) => error.to_compile_error().into(),
    }
}

fn expand(
    arguments: HandlerArguments,
    function: ItemFn,
) -> syn::Result<proc_macro2::TokenStream> {
    let (name, about) = parse_arguments(arguments)?;

    if !matches!(&function.vis, Visibility::Public(_)) {
        return Err(syn::Error::new_spanned(
            &function.sig.ident,
            "handler must be public",
        ));
    }

    let signature = &function.sig;
    if signature.asyncness.is_some()
        || signature.constness.is_some()
        || signature.unsafety.is_some()
        || signature.abi.is_some()
        || signature.variadic.is_some()
    {
        return Err(syn::Error::new_spanned(
            signature,
            "handler must be a safe synchronous Rust function",
        ));
    }
    if !signature.generics.params.is_empty() {
        return Err(syn::Error::new_spanned(
            &signature.generics,
            "generic handlers are not supported",
        ));
    }
    if signature.inputs.len() != 1 {
        return Err(syn::Error::new_spanned(
            &signature.inputs,
            "handler must accept exactly one `&str`",
        ));
    }

    let Some(first_argument) = signature.inputs.first() else {
        return Err(syn::Error::new_spanned(
            &signature.inputs,
            "handler must accept exactly one `&str`",
        ));
    };
    let FnArg::Typed(argument) = first_argument else {
        return Err(syn::Error::new_spanned(
            &signature.inputs,
            "methods are not supported",
        ));
    };
    if !is_shared_str_reference(argument.ty.as_ref()) {
        return Err(syn::Error::new_spanned(
            &argument.ty,
            "handler parameter must be `&str`",
        ));
    }
    if !returns_result(&signature.output) {
        return Err(syn::Error::new_spanned(
            &signature.output,
            "handler must return `Result<_, _>`",
        ));
    }

    let function_ident = &signature.ident;
    let metadata_ident = format_ident!(
        "{}_HANDLER",
        function_ident.to_string().to_uppercase()
    );

    Ok(quote! {
        #function

        pub const #metadata_ident: (
            &str,
            &str,
            fn(&str) -> ::std::result::Result<
                ::std::string::String,
                ::std::string::String,
            >,
        ) = (#name, #about, #function_ident);
    })
}
