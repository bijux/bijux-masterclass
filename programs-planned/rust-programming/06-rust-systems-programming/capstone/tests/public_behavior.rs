
use framevault::{Archive, Entry, EntryKind, Limits, LogicalPath, decode, encode};

#[test]
fn public_codec_round_trip_preserves_order_and_bytes() {
    let archive = Archive::from_entries(vec![
        Entry::new(
            EntryKind::File,
            LogicalPath::parse("alpha.bin").expect("valid path"),
            vec![0, 1, 2, 255],
        ),
        Entry::new(
            EntryKind::CommandCapture,
            LogicalPath::parse("captures/run.fvcmd").expect("valid path"),
            b"opaque-capture".to_vec(),
        ),
    ])
    .expect("unique fixture");

    let bytes = encode(&archive, Limits::default()).expect("encode succeeds");
    let decoded = decode(&bytes, Limits::default()).expect("decode succeeds");
    assert_eq!(decoded, archive);
    assert_eq!(decoded.entries()[0].name().as_str(), "alpha.bin");
    assert_eq!(decoded.entries()[1].kind(), EntryKind::CommandCapture);
}

#[test]
fn logical_path_policy_rejects_cross_platform_escape_spellings() {
    for candidate in ["/root", "../root", "a/../b", "a\\b", "C:/root", "a//b"] {
        assert!(LogicalPath::parse(candidate).is_err(), "accepted {candidate:?}");
    }
}
