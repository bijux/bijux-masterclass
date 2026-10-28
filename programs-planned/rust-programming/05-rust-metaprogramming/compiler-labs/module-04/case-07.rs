struct Vec;

macro_rules! make {
    () => {
        ::std::vec::Vec::<u8>::new()
    };
}

fn main() {
    let _shadow = Vec;
    let values = make!();
    assert!(values.is_empty());
}
