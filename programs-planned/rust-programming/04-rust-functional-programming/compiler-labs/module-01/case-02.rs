fn main() {
    let token = String::from("token");
    let consume = move || token;
    let _first = consume();
    let _second = consume();
}
