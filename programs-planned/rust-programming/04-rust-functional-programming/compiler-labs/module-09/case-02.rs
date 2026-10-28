fn choose(flag: bool) -> impl Fn(i32) -> i32 {
    let offset = 1;
    let factor = 2;
    if flag {
        move |value| value + offset
    } else {
        move |value| value * factor
    }
}

fn main() {
    let _ = choose(true);
}
