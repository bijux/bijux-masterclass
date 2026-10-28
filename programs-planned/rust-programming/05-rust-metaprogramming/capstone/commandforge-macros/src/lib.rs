#![forbid(unsafe_code)]

use proc_macro::TokenStream;
use quote::{format_ident, quote};
use std::collections::BTreeMap;
use syn::ext::IdentExt;
use syn::parse::{Parse, ParseStream};
use syn::punctuated::Punctuated;
use syn::{
    braced, parse_macro_input, parse_quote, Attribute, Data, DeriveInput, Expr,
    ExprLit, Fields, FnArg, Ident, ItemFn, Lit, LitStr, MetaNameValue,
    Path, ReturnType, Token, Type, Visibility, WherePredicate,
};

#[proc_macro_derive(CommandArgs, attributes(arg))]
pub fn derive_command_args(input: TokenStream) -> TokenStream {
    match expand_command_args(parse_macro_input!(input as DeriveInput)) {
        Ok(tokens) => tokens.into(),
        Err(error) => error.to_compile_error().into(),
    }
}

#[derive(Default)]
struct ArgumentPolicy {
    long: Option<LitStr>,
    help: Option<LitStr>,
    default: Option<LitStr>,
}

fn parse_argument_policy(attributes: &[Attribute]) -> syn::Result<ArgumentPolicy> {
    let mut policy = ArgumentPolicy::default();
    for attribute in attributes {
        if !attribute.path().is_ident("arg") {
            continue;
        }
        attribute.parse_nested_meta(|meta| {
            if meta.path.is_ident("long") {
                if policy.long.is_some() {
                    return Err(meta.error("duplicate `long`"));
                }
                let value: LitStr = meta.value()?.parse()?;
                if value.value().is_empty() {
                    return Err(syn::Error::new(value.span(), "long name must not be empty"));
                }
                policy.long = Some(value);
                return Ok(());
            }
            if meta.path.is_ident("help") {
                if policy.help.is_some() {
                    return Err(meta.error("duplicate `help`"));
                }
                let value: LitStr = meta.value()?.parse()?;
                if value.value().is_empty() {
                    return Err(syn::Error::new(value.span(), "help text must not be empty"));
                }
                policy.help = Some(value);
                return Ok(());
            }
            if meta.path.is_ident("default") {
                if policy.default.is_some() {
                    return Err(meta.error("duplicate `default`"));
                }
                policy.default = Some(meta.value()?.parse()?);
                return Ok(());
            }
            Err(meta.error("expected `long`, `help`, or `default`"))
        })?;
    }
    Ok(policy)
}

fn option_inner(ty: &Type) -> Option<&Type> {
    let Type::Path(path) = ty else { return None };
    if path.qself.is_some() || path.path.segments.len() != 1 {
        return None;
    }
    let segment = path.path.segments.last()?;
    if segment.ident != "Option" {
        return None;
    }
    let syn::PathArguments::AngleBracketed(arguments) = &segment.arguments else {
        return None;
    };
    if arguments.args.len() != 1 {
        return None;
    }
    match arguments.args.first()? {
        syn::GenericArgument::Type(inner) => Some(inner),
        _ => None,
    }
}

struct ParsedField {
    ident: Ident,
    declared_ty: Type,
    parse_ty: Type,
    optional: bool,
    long: LitStr,
    help: LitStr,
    default: Option<LitStr>,
}

fn expand_command_args(input: DeriveInput) -> syn::Result<proc_macro2::TokenStream> {
    let type_ident = input.ident;
    let named_fields = match input.data {
        Data::Struct(data) => match data.fields {
            Fields::Named(fields) => fields.named,
            other => {
                return Err(syn::Error::new_spanned(
                    other,
                    "CommandArgs supports named-field structs only",
                ));
            }
        },
        Data::Enum(data) => {
            return Err(syn::Error::new_spanned(
                data.enum_token,
                "CommandArgs supports structs only",
            ));
        }
        Data::Union(data) => {
            return Err(syn::Error::new_spanned(
                data.union_token,
                "CommandArgs supports structs only",
            ));
        }
    };

    let mut parsed_fields = Vec::new();
    let mut errors: Option<syn::Error> = None;

    for field in named_fields {
        let Some(field_ident) = field.ident.clone() else {
            continue;
        };
        match parse_argument_policy(&field.attrs) {
            Ok(policy) => {
                let default_long = field_ident.unraw().to_string().replace('_', "-");
                let long = policy.long.unwrap_or_else(|| {
                    LitStr::new(&default_long, field_ident.span())
                });
                if long.value().starts_with('-') || long.value().chars().any(char::is_whitespace) {
                    let error = syn::Error::new(
                        long.span(),
                        "long name must not contain leading dashes or whitespace",
                    );
                    if let Some(all) = &mut errors { all.combine(error); } else { errors = Some(error); }
                    continue;
                }
                let help = policy.help.unwrap_or_else(|| {
                    LitStr::new("value", field_ident.span())
                });
                let (parse_ty, optional) = option_inner(&field.ty)
                    .map(|inner| (inner.clone(), true))
                    .unwrap_or_else(|| (field.ty.clone(), false));
                if optional && policy.default.is_some() {
                    let error = syn::Error::new(
                        field_ident.span(),
                        "optional fields cannot also declare a default",
                    );
                    if let Some(all) = &mut errors { all.combine(error); } else { errors = Some(error); }
                    continue;
                }
                parsed_fields.push(ParsedField {
                    ident: field_ident,
                    declared_ty: field.ty,
                    parse_ty,
                    optional,
                    long,
                    help,
                    default: policy.default,
                });
            }
            Err(error) => {
                if let Some(all) = &mut errors { all.combine(error); } else { errors = Some(error); }
            }
        }
    }
    let mut first_long_span: BTreeMap<String, proc_macro2::Span> = BTreeMap::new();
    for field in &parsed_fields {
        let long = field.long.value();
        if let Some(first_span) = first_long_span.get(&long).copied() {
            let mut error = syn::Error::new(
                field.long.span(),
                format!("duplicate long option `--{long}`"),
            );
            error.combine(syn::Error::new(first_span, "first declared here"));
            if let Some(all) = &mut errors {
                all.combine(error);
            } else {
                errors = Some(error);
            }
        } else {
            first_long_span.insert(long, field.long.span());
        }
    }

    if let Some(error) = errors {
        return Err(error);
    }

    let mut generics = input.generics;
    for field in &parsed_fields {
        let parse_ty = &field.parse_ty;
        let predicate: WherePredicate = parse_quote!(
            #parse_ty: ::std::str::FromStr
        );
        let error_predicate: WherePredicate = parse_quote!(
            <#parse_ty as ::std::str::FromStr>::Err: ::std::fmt::Display
        );
        generics.make_where_clause().predicates.push(predicate);
        generics.make_where_clause().predicates.push(error_predicate);
    }
    let (impl_generics, type_generics, where_clause) = generics.split_for_impl();

    let declarations = parsed_fields.iter().map(|field| {
        let ident = &field.ident;
        let parse_ty = &field.parse_ty;
        quote!(let mut #ident: ::std::option::Option<#parse_ty> = ::std::option::Option::None;)
    });

    let match_arms = parsed_fields.iter().map(|field| {
        let ident = &field.ident;
        let parse_ty = &field.parse_ty;
        let flag = LitStr::new(&format!("--{}", field.long.value()), field.long.span());
        quote! {
            #flag => {
                if #ident.is_some() {
                    return ::std::result::Result::Err(
                        ::commandforge::ArgError::DuplicateArgument { flag: #flag }
                    );
                }
                let raw_value = iterator.next().ok_or(
                    ::commandforge::ArgError::MissingValue { flag: #flag }
                )?;
                let parsed_value = raw_value.parse::<#parse_ty>().map_err(|error| {
                    ::commandforge::ArgError::InvalidValue {
                        flag: #flag,
                        value: raw_value.clone(),
                        message: error.to_string(),
                    }
                })?;
                #ident = ::std::option::Option::Some(parsed_value);
            }
        }
    });

    let finalizers = parsed_fields.iter().map(|field| {
        let ident = &field.ident;
        let declared_ty = &field.declared_ty;
        let flag = LitStr::new(&format!("--{}", field.long.value()), field.long.span());
        if field.optional {
            quote!(let #ident: #declared_ty = #ident;)
        } else if let Some(default) = &field.default {
            let parse_ty = &field.parse_ty;
            quote! {
                let #ident: #declared_ty = match #ident {
                    ::std::option::Option::Some(value) => value,
                    ::std::option::Option::None => #default.parse::<#parse_ty>().map_err(|error| {
                        ::commandforge::ArgError::InvalidDefault {
                            flag: #flag,
                            value: #default,
                            message: error.to_string(),
                        }
                    })?,
                };
            }
        } else {
            quote! {
                let #ident: #declared_ty = #ident.ok_or(
                    ::commandforge::ArgError::MissingRequired { flag: #flag }
                )?;
            }
        }
    });

    let field_names = parsed_fields.iter().map(|field| &field.ident);
    let usage = parsed_fields
        .iter()
        .map(|field| {
            let flag = format!("--{}", field.long.value());
            if field.optional || field.default.is_some() {
                format!("[{flag} <value>]")
            } else {
                format!("{flag} <value>")
            }
        })
        .collect::<Vec<_>>()
        .join(" ");
    let usage = LitStr::new(&usage, type_ident.span());

    let option_rows = parsed_fields.iter().map(|field| {
        let flag = LitStr::new(&format!("--{}", field.long.value()), field.long.span());
        let help = &field.help;
        let required = !(field.optional || field.default.is_some());
        quote! {
            ::commandforge::ArgumentSpec {
                flag: #flag,
                help: #help,
                required: #required,
            }
        }
    });

    Ok(quote! {
        impl #impl_generics ::commandforge::CommandArgs for #type_ident #type_generics #where_clause {
            const USAGE: &'static str = #usage;
            const ARGUMENTS: &'static [::commandforge::ArgumentSpec] = &[#(#option_rows),*];

            fn decode(
                raw: &[::std::string::String],
            ) -> ::std::result::Result<Self, ::commandforge::ArgError> {
                #(#declarations)*
                let mut iterator = raw.iter();
                while let ::std::option::Option::Some(flag) = iterator.next() {
                    match flag.as_str() {
                        #(#match_arms)*
                        _ => {
                            return ::std::result::Result::Err(
                                ::commandforge::ArgError::UnknownArgument {
                                    flag: flag.clone(),
                                }
                            );
                        }
                    }
                }
                #(#finalizers)*
                ::std::result::Result::Ok(Self { #(#field_names),* })
            }
        }
    })
}

#[proc_macro_attribute]
pub fn command_handler(arguments: TokenStream, item: TokenStream) -> TokenStream {
    let arguments = parse_macro_input!(arguments as HandlerArguments);
    let function = parse_macro_input!(item as ItemFn);
    match expand_handler(arguments, function) {
        Ok(tokens) => tokens.into(),
        Err(error) => error.to_compile_error().into(),
    }
}

struct HandlerArguments {
    items: Punctuated<MetaNameValue, Token![,]>,
}

impl Parse for HandlerArguments {
    fn parse(input: ParseStream<'_>) -> syn::Result<Self> {
        Ok(Self { items: Punctuated::parse_terminated(input)? })
    }
}

fn string_meta(item: MetaNameValue) -> syn::Result<(Ident, LitStr)> {
    let Some(identifier) = item.path.get_ident().cloned() else {
        return Err(syn::Error::new_spanned(item.path, "expected a simple metadata key"));
    };
    let value = match item.value {
        Expr::Lit(ExprLit {
            lit: Lit::Str(value),
            ..
        }) => value,
        other => {
            return Err(syn::Error::new_spanned(
                other,
                "expected a string literal",
            ));
        }
    };
    Ok((identifier, value))
}

fn expand_handler(
    arguments: HandlerArguments,
    function: ItemFn,
) -> syn::Result<proc_macro2::TokenStream> {
    let mut about = None;
    for item in arguments.items {
        let (key, value) = string_meta(item)?;
        if value.value().is_empty() {
            return Err(syn::Error::new(value.span(), "metadata value must not be empty"));
        }
        match key.to_string().as_str() {
            "about" => {
                if about.replace(value).is_some() {
                    return Err(syn::Error::new(key.span(), "duplicate `about`"));
                }
            }
            _ => return Err(syn::Error::new(key.span(), "expected `about`")),
        }
    }
    let about = about.ok_or_else(|| {
        syn::Error::new(proc_macro2::Span::call_site(), "missing `about`")
    })?;

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
            "handler must accept exactly one owned argument value",
        ));
    }
    let Some(first_argument) = signature.inputs.first() else {
        return Err(syn::Error::new_spanned(
            &signature.inputs,
            "handler must accept exactly one owned argument value",
        ));
    };
    let FnArg::Typed(argument) = first_argument else {
        return Err(syn::Error::new_spanned(
            &signature.inputs,
            "methods are not supported",
        ));
    };
    if matches!(argument.ty.as_ref(), Type::Reference(_)) {
        return Err(syn::Error::new_spanned(
            &argument.ty,
            "handler argument must be owned so the generated decoder can construct it",
        ));
    }
    if !matches!(&signature.output, ReturnType::Type(_, _)) {
        return Err(syn::Error::new_spanned(
            &signature.output,
            "handler must declare an explicit result type",
        ));
    }

    let argument_type = argument.ty.as_ref();
    let function_ident = &signature.ident;
    let wrapper_ident = format_ident!("__commandforge_invoke_{}", function_ident);
    let descriptor_ident = format_ident!(
        "{}_HANDLER",
        function_ident.to_string().to_uppercase()
    );

    Ok(quote! {
        #function

        fn #wrapper_ident(
            raw: &[::std::string::String],
        ) -> ::std::result::Result<::std::string::String, ::commandforge::CommandError> {
            let arguments = <#argument_type as ::commandforge::CommandArgs>::decode(raw)?;
            #function_ident(arguments)
        }

        pub const #descriptor_ident: ::commandforge::HandlerDescriptor =
            ::commandforge::HandlerDescriptor {
                about: #about,
                usage: <#argument_type as ::commandforge::CommandArgs>::USAGE,
                arguments: <#argument_type as ::commandforge::CommandArgs>::ARGUMENTS,
                invoke: #wrapper_ident,
            };
    })
}

#[proc_macro]
pub fn command_catalog(input: TokenStream) -> TokenStream {
    let input = parse_macro_input!(input as CatalogInput);
    match expand_catalog(input) {
        Ok(tokens) => tokens.into(),
        Err(error) => error.to_compile_error().into(),
    }
}

struct CatalogEntry {
    name: LitStr,
    descriptor: Path,
}

struct CatalogInput {
    table_visibility: Visibility,
    table_name: Ident,
    lookup_visibility: Visibility,
    lookup_name: Ident,
    entries: Vec<CatalogEntry>,
}

impl Parse for CatalogInput {
    fn parse(input: ParseStream<'_>) -> syn::Result<Self> {
        let table_visibility = input.parse()?;
        input.parse::<Token![static]>()?;
        let table_name = input.parse()?;
        input.parse::<Token![;]>()?;

        let lookup_visibility = input.parse()?;
        input.parse::<Token![fn]>()?;
        let lookup_name = input.parse()?;
        input.parse::<Token![;]>()?;

        let content;
        braced!(content in input);
        let mut entries = Vec::new();
        while !content.is_empty() {
            let name = content.parse()?;
            content.parse::<Token![=>]>()?;
            let descriptor = content.parse()?;
            content.parse::<Token![;]>()?;
            entries.push(CatalogEntry { name, descriptor });
        }

        Ok(Self {
            table_visibility,
            table_name,
            lookup_visibility,
            lookup_name,
            entries,
        })
    }
}

fn expand_catalog(input: CatalogInput) -> syn::Result<proc_macro2::TokenStream> {
    if input.entries.is_empty() {
        return Err(syn::Error::new(
            input.table_name.span(),
            "command catalog must contain at least one entry",
        ));
    }
    let mut seen: BTreeMap<String, proc_macro2::Span> = BTreeMap::new();
    let mut errors: Option<syn::Error> = None;
    for entry in &input.entries {
        let name = entry.name.value();
        if name.is_empty() {
            let error = syn::Error::new(entry.name.span(), "command name must not be empty");
            if let Some(all) = &mut errors {
                all.combine(error);
            } else {
                errors = Some(error);
            }
            continue;
        }
        if name.chars().any(char::is_whitespace) || name.starts_with('-') {
            let error = syn::Error::new(
                entry.name.span(),
                "command name must not contain whitespace or start with `-`",
            );
            if let Some(all) = &mut errors {
                all.combine(error);
            } else {
                errors = Some(error);
            }
            continue;
        }
        if let Some(first_span) = seen.get(&name).copied() {
            let mut error = syn::Error::new(entry.name.span(), "duplicate command name");
            error.combine(syn::Error::new(first_span, "first declared here"));
            if let Some(all) = &mut errors {
                all.combine(error);
            } else {
                errors = Some(error);
            }
        } else {
            seen.insert(name, entry.name.span());
        }
    }
    if let Some(error) = errors {
        return Err(error);
    }

    let table_visibility = input.table_visibility;
    let table_name = input.table_name;
    let lookup_visibility = input.lookup_visibility;
    let lookup_name = input.lookup_name;
    let rows = input.entries.iter().map(|entry| {
        let name = &entry.name;
        let descriptor = &entry.descriptor;
        quote! {
            ::commandforge::CommandSpec {
                name: #name,
                handler: #descriptor,
            }
        }
    });

    let lookup_arms = input.entries.iter().enumerate().map(|(index, entry)| {
        let name = &entry.name;
        let index = syn::Index::from(index);
        quote!(#name => ::std::option::Option::Some(&#table_name[#index]))
    });

    Ok(quote! {
        #table_visibility static #table_name: &[::commandforge::CommandSpec] = &[
            #(#rows),*
        ];

        #lookup_visibility fn #lookup_name(
            name: &str,
        ) -> ::std::option::Option<&'static ::commandforge::CommandSpec> {
            match name {
                #(#lookup_arms,)*
                _ => ::std::option::Option::None,
            }
        }
    })
}
