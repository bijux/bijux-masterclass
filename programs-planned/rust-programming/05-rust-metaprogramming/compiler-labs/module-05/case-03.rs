macro_rules! catalog {
    ($($name:ident = $code:literal => $message:literal),+ $(,)?) => {
        #[derive(Clone, Copy, PartialEq, Eq)]
        enum Diagnostic {
            $( $name ),+
        }

        impl Diagnostic {
            fn code(self) -> u16 {
                match self {
                    $( Self::$name => $code ),+
                }
            }

            fn from_code(code: u16) -> Option<Self> {
                match code {
                    $( $code => Some(Self::$name), )+
                    _ => None,
                }
            }
        }
    };
}

catalog!(
    Missing = 1001 => "missing",
    Invalid = 1002 => "invalid",
);

fn main() {
    let diagnostic = Diagnostic::from_code(1002).expect("known code");
    assert!(matches!(diagnostic, Diagnostic::Invalid));
    assert_eq!(diagnostic.code(), 1002);
}
