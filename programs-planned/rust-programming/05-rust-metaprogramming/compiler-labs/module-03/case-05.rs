macro_rules! machine {
    (
        $name:ident {
            states [$( $state:ident ),+ $(,)?];
            transitions { $( $from:ident => $to:ident; )* }
        }
    ) => {
        #[derive(Clone, Copy, PartialEq, Eq)]
        enum $name {
            $( $state ),+
        }

        impl $name {
            fn next(self) -> Option<Self> {
                match self {
                    $( Self::$from => Some(Self::$to), )*
                    _ => None,
                }
            }
        }
    };
}

machine! {
    State {
        states [Draft, Review, Published];
        transitions {
            Draft => Review;
            Review => Published;
        }
    }
}

fn main() {
    assert!(matches!(State::Draft.next(), Some(State::Review)));
}
