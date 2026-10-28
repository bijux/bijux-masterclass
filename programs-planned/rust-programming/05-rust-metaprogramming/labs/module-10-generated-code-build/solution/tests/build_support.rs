#[path = "../build_support.rs"]
mod build_support;

#[test]
fn parsing_and_rendering_are_separate_and_deterministic() {
    let input = "list\t10\tList all records\nshow\t20\tShow one record\n";
    let rows = build_support::parse(input).expect("valid rows");
    assert_eq!(rows.iter().map(|row| row.name.as_str()).collect::<Vec<_>>(), ["list", "show"]);
    assert_eq!(build_support::render(&rows), build_support::render(&rows));
}

#[test]
fn invalid_rows_report_physical_line_context() {
    let error = build_support::parse("list\t10\tList\nlist\t20\tAgain\n").unwrap_err();
    assert!(error.contains("line 2"));
    assert!(error.contains("first declared on line 1"));
    assert!(build_support::parse("").unwrap_err().contains("at least one row"));
}

#[test]
fn a_third_duplicate_still_points_to_the_original_declaration() {
    let input = concat!(
        "list\t10\tFirst\n",
        "list\t20\tSecond\n",
        "list\t30\tThird\n",
    );
    let error = build_support::parse(input).expect_err("duplicate name");
    assert!(error.contains("line 2"));
    assert!(error.contains("first declared on line 1"));
}

#[test]
fn generated_file_replacement_writes_complete_bytes() {
    let directory = std::env::temp_dir().join(format!(
        "course5-lab50-build-support-{}",
        std::process::id(),
    ));
    let _ = std::fs::remove_dir_all(&directory);
    std::fs::create_dir_all(&directory).expect("create temporary directory");
    let destination = directory.join("generated.rs");

    build_support::write_generated(&destination, "pub const VALUE: u8 = 7;\n")
        .expect("replace generated file");
    assert_eq!(
        std::fs::read_to_string(&destination).expect("read generated file"),
        "pub const VALUE: u8 = 7;\n",
    );

    std::fs::remove_dir_all(directory).expect("remove temporary directory");
}
