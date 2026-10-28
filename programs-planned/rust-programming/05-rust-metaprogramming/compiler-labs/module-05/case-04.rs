#![allow(dead_code)]
#![deny(unreachable_patterns)]

macro_rules! catalog {
    ($($name:ident = $code:literal),+) => {
        enum Diagnostic {
            $( $name ),+
        }

        impl Diagnostic {
            fn from_code(code: u16) -> Option<Self> {
                match code {
                    $( $code => Some(Self::$name), )+
                    _ => None,
                }
            }
        }
    };
}

catalog!(A = 1, B = 1);

fn main() {}
