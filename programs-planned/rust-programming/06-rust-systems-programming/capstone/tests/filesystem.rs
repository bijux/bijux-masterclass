
use framevault::path_policy::write_new_file;
use framevault::store::{load, save_atomic};
use framevault::{Archive, Entry, EntryKind, Limits, LogicalPath};
use std::fs;
use std::path::PathBuf;
use std::time::{SystemTime, UNIX_EPOCH};

fn fixture_root(label: &str) -> PathBuf {
    let stamp = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .expect("clock after epoch")
        .as_nanos();
    std::env::temp_dir().join(format!("framevault-it-{label}-{}-{stamp}", std::process::id()))
}

#[test]
fn archive_storage_and_extraction_preserve_payload() {
    let root = fixture_root("filesystem");
    let archive_path = root.join("archive.fv");
    let extraction = root.join("out");
    let archive = Archive::from_entries(vec![Entry::new(
        EntryKind::File,
        LogicalPath::parse("docs/guide.bin").expect("valid path"),
        vec![0, 4, 8, 255],
    )])
    .expect("unique fixture");

    save_atomic(&archive_path, &archive, Limits::default()).expect("save succeeds");
    let loaded = load(&archive_path, Limits::default()).expect("load succeeds");
    let destination = write_new_file(
        &extraction,
        loaded.entries()[0].name(),
        loaded.entries()[0].payload(),
    )
    .expect("extraction succeeds");
    assert_eq!(fs::read(destination).expect("read extraction"), vec![0, 4, 8, 255]);
    fs::remove_dir_all(root).expect("remove fixture");
}
