#[macro_export]
macro_rules! diagnostic_catalog {
    ($vis:vis enum $name:ident { $( $variant:ident = $code:literal => $message:literal; )+ }) => {
        #[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
        $vis enum $name { $( $variant ),+ }
        impl $name {
            $vis const ALL: &'static [Self] = &[$( Self::$variant ),+];
            $vis const fn code(self) -> u16 {
                match self { $( Self::$variant => $code ),+ }
            }
            $vis const fn message(self) -> &'static str {
                match self { $( Self::$variant => $message ),+ }
            }
            $vis const fn from_code(code: u16) -> Option<Self> {
                match code { $( $code => Some(Self::$variant), )+ _ => None }
            }
        }
        impl ::std::fmt::Display for $name {
            fn fmt(&self, formatter: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
                formatter.write_str(self.message())
            }
        }
    };
    ($vis:vis enum $name:ident { $variant:ident => $message:literal; $($rest:tt)* }) => {
        compile_error!("diagnostic code is required: `Variant = CODE => MESSAGE;`")
    };
    ($($bad:tt)*) => { compile_error!("invalid diagnostic catalog syntax") };
}

diagnostic_catalog! {
    pub enum Diagnostic {
        UnknownCommand = 1001 => "unknown command";
        ArgumentFailure = 1002 => "argument decoding failed";
        DomainFailure = 1003 => "command domain validation failed";
        UsageFailure = 1004 => "top-level usage is invalid";
    }
}
