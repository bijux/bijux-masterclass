#![forbid(unsafe_code)]

#[macro_export]
macro_rules! state_machine {
    (
        $vis:vis enum $name:ident {
            states [$( $state:ident ),+ $(,)?];
            transitions { $( $from:ident => $to:ident; )* }
        }
    ) => {
        #[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
        $vis enum $name {
            $( $state ),+
        }

        impl $name {
            $vis const fn can_transition(self, next: Self) -> bool {
                $crate::state_machine!(
                    @check self, next;
                    $( $from => $to; )*
                )
            }
        }
    };

    (@check $current:ident, $next:ident;) => {
        false
    };

    (
        @check $current:ident, $next:ident;
        $from:ident => $to:ident;
        $( $rest_from:ident => $rest_to:ident; )*
    ) => {
        if matches!(($current, $next), (Self::$from, Self::$to)) {
            true
        } else {
            $crate::state_machine!(
                @check $current, $next;
                $( $rest_from => $rest_to; )*
            )
        }
    };

    ($($bad:tt)*) => {
        compile_error!(
            "expected `vis enum Name { states [A, B]; transitions { A => B; } }`"
        )
    };
}

state_machine! {
    pub enum Publication {
        states [Draft, Review, Published];
        transitions {
            Draft => Review;
            Review => Draft;
            Review => Published;
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn legal_edges_are_accepted() {
        assert!(Publication::Draft.can_transition(Publication::Review));
        assert!(Publication::Review.can_transition(Publication::Published));
    }

    #[test]
    fn illegal_edges_are_rejected() {
        assert!(!Publication::Draft.can_transition(Publication::Published));
        assert!(!Publication::Published.can_transition(Publication::Draft));
    }
}
