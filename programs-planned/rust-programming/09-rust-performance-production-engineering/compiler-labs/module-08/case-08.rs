#[derive(Debug)]
struct Credentials {
    token: String,
}

fn main() {
    let credentials = Credentials {
        token: "secret".into(),
    };
    println!("{credentials:?}");
    assert_eq!(credentials.token.len(), 6);
}
