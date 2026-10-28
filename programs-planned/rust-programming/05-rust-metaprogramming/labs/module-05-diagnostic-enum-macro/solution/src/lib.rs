#![forbid(unsafe_code)]

#[macro_export]
macro_rules! diagnostic_enum {
    (
        $vis:vis enum $name:ident {
            $( $variant:ident = $code:literal => $message:literal; )+
        }
    ) => {
        #[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
        $vis enum $name {
            $( $variant ),+
        }

        impl $name {
            $vis const ALL: &'static [Self] = &[
                $( Self::$variant ),+
            ];

            $vis const fn code(self) -> u16 {
                match self {
                    $( Self::$variant => $code ),+
                }
            }

            $vis const fn message(self) -> &'static str {
                match self {
                    $( Self::$variant => $message ),+
                }
            }

            $vis const fn from_code(code: u16) -> Option<Self> {
                match code {
                    $( $code => Some(Self::$variant), )+
                    _ => None,
                }
            }
        }

        impl ::std::fmt::Display for $name {
            fn fmt(
                &self,
                formatter: &mut ::std::fmt::Formatter<'_>,
            ) -> ::std::fmt::Result {
                formatter.write_str(self.message())
            }
        }
    };

    (
        $vis:vis enum $name:ident {
            $variant:ident => $message:literal;
            $($rest:tt)*
        }
    ) => {
        compile_error!(
            "diagnostic code is required: `Variant = CODE => MESSAGE;`"
        )
    };

    (
        $vis:vis enum $name:ident {
            $variant:ident = $code:literal;
            $($rest:tt)*
        }
    ) => {
        compile_error!("diagnostic message is required after `=>`")
    };

    ($($bad:tt)*) => {
        compile_error!("invalid diagnostic catalog syntax")
    };
}

diagnostic_enum! {
    pub enum Diagnostic {
        MissingField = 1001 => "missing field";
        InvalidNumber = 1002 => "invalid number";
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn every_code_round_trips() {
        for &diagnostic in Diagnostic::ALL {
            assert_eq!(
                Diagnostic::from_code(diagnostic.code()),
                Some(diagnostic),
            );
        }
    }

    #[test]
    fn unknown_code_is_absent() {
        assert_eq!(Diagnostic::from_code(9999), None);
    }

    #[test]
    fn display_and_authored_order_are_stable() {
        assert_eq!(
            Diagnostic::ALL,
            &[Diagnostic::MissingField, Diagnostic::InvalidNumber],
        );
        assert_eq!(Diagnostic::InvalidNumber.to_string(), "invalid number");
    }
}
