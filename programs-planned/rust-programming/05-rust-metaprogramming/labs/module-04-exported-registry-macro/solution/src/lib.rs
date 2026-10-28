#![forbid(unsafe_code)]

#[derive(Debug, Clone, Copy)]
pub struct Entry {
    pub name: &'static str,
    pub handler: fn(&str) -> String,
}

impl Entry {
    pub const fn new(
        name: &'static str,
        handler: fn(&str) -> String,
    ) -> Self {
        Self { name, handler }
    }
}

pub fn find(entries: &[Entry], name: &str) -> Option<Entry> {
    entries.iter().copied().find(|entry| entry.name == name)
}

#[macro_export]
macro_rules! command_registry {
    (
        $vis:vis static $name:ident {
            $( $command:literal => $handler:path; )*
        }
    ) => {
        $vis static $name: &[$crate::Entry] = &[
            $( $crate::Entry::new($command, $handler), )*
        ];
    };
    ($($bad:tt)*) => {
        compile_error!(
            "expected `vis static NAME { \"command\" => handler::path; }`"
        )
    };
}
