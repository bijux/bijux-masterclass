#[derive(Clone, Copy)]
enum Outcome {
    Ok,
    Invalid,
    Overloaded,
}

impl Outcome {
    fn label(self) -> &'static str {
        match self {
            Self::Ok => "ok",
            Self::Invalid => "invalid",
            Self::Overloaded => "overloaded",
        }
    }
}

fn main() {
    assert_eq!(Outcome::Ok.label(), "ok");
    assert_eq!(Outcome::Invalid.label(), "invalid");
    assert_eq!(Outcome::Overloaded.label(), "overloaded");
}
