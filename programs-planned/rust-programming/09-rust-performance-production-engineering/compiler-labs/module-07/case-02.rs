#[derive(Clone, Copy)]
enum Failure {
    Transient,
    Permanent,
}

fn retry(failure: Failure) -> bool {
    matches!(failure, Failure::Transient)
}

fn main() {
    assert!(retry(Failure::Transient));
    assert!(!retry(Failure::Permanent));
}
