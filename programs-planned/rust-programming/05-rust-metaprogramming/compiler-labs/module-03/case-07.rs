macro_rules! entry {
    (name = $name:literal;) => {
        $name
    };
    ($($bad:tt)*) => {
        compile_error!("expected `name = \\\"...\\\";`")
    };
}

fn main() {
    assert_eq!(entry!(name = "ok";), "ok");
}
