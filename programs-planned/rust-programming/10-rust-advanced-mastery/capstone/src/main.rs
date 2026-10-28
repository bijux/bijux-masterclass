fn main() {
    match axiomstore::run(std::env::args_os()) {
        Ok(output) => print!("{output}"),
        Err(error) => {
            eprintln!("error: {error}");
            let code = if matches!(error, axiomstore::StoreError::Usage(_)) {
                2
            } else {
                1
            };
            std::process::exit(code);
        }
    }
}
