
use std::fs;
use std::path::PathBuf;
use std::process::Command;
use std::time::{SystemTime, UNIX_EPOCH};

fn fixture_root() -> PathBuf {
    let stamp = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .expect("clock after epoch")
        .as_nanos();
    std::env::temp_dir().join(format!("framevault-cli-{}-{stamp}", std::process::id()))
}

#[test]
fn create_list_verify_and_extract_form_one_product_route() {
    let binary = env!("CARGO_BIN_EXE_framevault");
    let root = fixture_root();
    fs::create_dir_all(&root).expect("create fixture root");
    let source = root.join("source.bin");
    let archive = root.join("archive.fv");
    let output = root.join("out");
    fs::write(&source, [0_u8, 1, 2, 255]).expect("write source");

    let create = Command::new(binary)
        .arg("create")
        .arg(&archive)
        .arg("--entry")
        .arg("nested/source.bin")
        .arg(&source)
        .output()
        .expect("run create");
    assert!(create.status.success(), "{}", String::from_utf8_lossy(&create.stderr));

    let list = Command::new(binary)
        .arg("list")
        .arg(&archive)
        .output()
        .expect("run list");
    assert!(list.status.success());
    let listing = String::from_utf8(list.stdout).expect("UTF-8 listing");
    assert!(listing.contains("nested/source.bin"));
    assert!(listing.contains("file"));

    let verify = Command::new(binary)
        .arg("verify")
        .arg(&archive)
        .output()
        .expect("run verify");
    assert!(verify.status.success());
    assert!(String::from_utf8(verify.stdout).expect("UTF-8 verify").contains("entries=1"));

    let extract = Command::new(binary)
        .arg("extract")
        .arg(&archive)
        .arg(&output)
        .output()
        .expect("run extract");
    assert!(extract.status.success(), "{}", String::from_utf8_lossy(&extract.stderr));
    assert_eq!(fs::read(output.join("nested/source.bin")).expect("read extraction"), [0, 1, 2, 255]);

    fs::remove_dir_all(root).expect("remove fixture");
}


#[test]
fn ordinary_source_paths_may_contain_equals_signs() {
    let binary = env!("CARGO_BIN_EXE_framevault");
    let root = fixture_root();
    fs::create_dir_all(&root).expect("create fixture root");
    let source = root.join("name=with-equals.bin");
    let archive = root.join("equals.fv");
    fs::write(&source, b"equals").expect("write source");

    let create = Command::new(binary)
        .arg("create")
        .arg(&archive)
        .arg(&source)
        .output()
        .expect("run create");
    assert!(create.status.success(), "{}", String::from_utf8_lossy(&create.stderr));

    let list = Command::new(binary)
        .arg("list")
        .arg(&archive)
        .output()
        .expect("run list");
    assert!(list.status.success());
    assert!(String::from_utf8(list.stdout)
        .expect("UTF-8 listing")
        .contains("name=with-equals.bin"));

    fs::remove_dir_all(root).expect("remove fixture");
}
