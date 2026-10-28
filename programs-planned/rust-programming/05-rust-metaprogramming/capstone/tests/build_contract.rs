#[path = "../build_support.rs"]
mod build_support;

use std::fs;

#[test]
fn parser_preserves_authored_order_and_renderer_is_deterministic() {
    let input = concat!(
        "SUCCESS\t0\tcompleted\n",
        "FAILURE\t1\trejected\n",
    );
    let rows = build_support::parse(input).expect("valid build table");
    assert_eq!(rows.iter().map(|row| row.name.as_str()).collect::<Vec<_>>(), ["SUCCESS", "FAILURE"]);

    let first = build_support::render(&rows);
    let second = build_support::render(&rows);
    assert_eq!(first, second);
    assert!(first.contains("pub const EXIT_SUCCESS: i32 = 0;"));
    assert!(first.contains("description: \"rejected\""));
}

#[test]
fn parser_reports_physical_lines_and_first_declarations() {
    let duplicate_name = concat!(
        "SUCCESS\t0\tcompleted\n",
        "SUCCESS\t1\tduplicate\n",
    );
    let error = build_support::parse(duplicate_name).unwrap_err();
    assert!(error.contains("line 2"));
    assert!(error.contains("first declared on line 1"));

    let third_duplicate = concat!(
        "SUCCESS\t0\tcompleted\n",
        "SUCCESS\t1\tsecond\n",
        "SUCCESS\t2\tthird\n",
    );
    let error = build_support::parse(third_duplicate).unwrap_err();
    assert!(error.contains("line 2"));
    assert!(error.contains("first declared on line 1"));

    let duplicate_code = concat!(
        "SUCCESS\t0\tcompleted\n",
        "OTHER\t0\tduplicate\n",
    );
    let error = build_support::parse(duplicate_code).unwrap_err();
    assert!(error.contains("duplicates code `0`"));
}

#[test]
fn parser_rejects_malformed_or_empty_tables() {
    assert!(build_support::parse("").unwrap_err().contains("at least one row"));
    assert!(build_support::parse("bad-row\n").unwrap_err().contains("line 1"));
    assert!(build_support::parse("lower\t1\tbad name\n").unwrap_err().contains("invalid exit-code name"));
    assert!(build_support::parse("TOO_BIG\t256\tbad code\n").unwrap_err().contains("outside 0..=255"));
}

#[test]
fn generated_file_replacement_writes_complete_bytes() {
    let directory = std::env::temp_dir().join(format!(
        "commandforge-build-contract-{}",
        std::process::id()
    ));
    let _ = fs::remove_dir_all(&directory);
    fs::create_dir_all(&directory).expect("create temporary directory");
    let destination = directory.join("generated.rs");

    build_support::write_generated(&destination, "pub const VALUE: u8 = 7;\n")
        .expect("write generated file");
    assert_eq!(
        fs::read_to_string(&destination).expect("read generated file"),
        "pub const VALUE: u8 = 7;\n"
    );

    fs::remove_dir_all(directory).expect("remove temporary directory");
}
