#![allow(dead_code, unused_imports, unused_variables)]
#[cfg(unix)] fn bytes(path: &std::path::Path) -> &[u8] { use std::os::unix::ffi::OsStrExt; path.as_os_str().as_bytes() } #[cfg(not(unix))] fn bytes(_path: &std::path::Path) -> &[u8] { &[] } fn main() { let _ = bytes(std::path::Path::new("a")); }
