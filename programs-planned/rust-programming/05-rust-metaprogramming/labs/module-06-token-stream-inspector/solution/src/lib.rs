#![forbid(unsafe_code)]

use proc_macro::{
    Delimiter, Group, Literal, Spacing, TokenStream, TokenTree,
};

fn delimiter_name(delimiter: Delimiter) -> &'static str {
    match delimiter {
        Delimiter::Parenthesis => "Paren",
        Delimiter::Brace => "Brace",
        Delimiter::Bracket => "Bracket",
        Delimiter::None => "None",
    }
}

fn spacing_name(spacing: Spacing) -> &'static str {
    match spacing {
        Spacing::Alone => "Alone",
        Spacing::Joint => "Joint",
    }
}

fn describe(stream: TokenStream) -> String {
    stream
        .into_iter()
        .map(|tree| match tree {
            TokenTree::Group(group) => describe_group(group),
            TokenTree::Ident(identifier) => format!("Ident({identifier})"),
            TokenTree::Punct(punctuation) => format!(
                "Punct({},{})",
                punctuation.as_char(),
                spacing_name(punctuation.spacing()),
            ),
            TokenTree::Literal(literal) => format!("Literal({literal})"),
        })
        .collect::<Vec<_>>()
        .join(" ")
}

fn describe_group(group: Group) -> String {
    format!(
        "Group({}:[{}])",
        delimiter_name(group.delimiter()),
        describe(group.stream()),
    )
}

#[proc_macro]
pub fn token_tree_shape(input: TokenStream) -> TokenStream {
    let description = describe(input);
    TokenStream::from(TokenTree::Literal(Literal::string(&description)))
}

#[proc_macro]
pub fn top_level_token_count(input: TokenStream) -> TokenStream {
    let count = input.into_iter().count();
    TokenStream::from(TokenTree::Literal(Literal::usize_unsuffixed(count)))
}
