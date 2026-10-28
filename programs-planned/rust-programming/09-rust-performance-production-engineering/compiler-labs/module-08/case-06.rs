struct Credentials {
    token: str,
}

fn require_sized<T: Sized>() {}

fn main() {
    require_sized::<Credentials>();
}
