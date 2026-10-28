#[derive(Clone, Copy)]
enum Capability {
    Read,
    Admin,
}

fn authorize(capability: Capability) -> bool {
    matches!(capability, Capability::Admin)
}

fn main() {
    assert!(!authorize(Capability::Read));
    assert!(authorize(Capability::Admin));
}
