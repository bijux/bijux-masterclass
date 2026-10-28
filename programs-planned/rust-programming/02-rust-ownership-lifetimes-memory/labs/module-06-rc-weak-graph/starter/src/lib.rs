//! Immutable shared-node baseline before graph topology is introduced.

use std::rc::Rc;

/// One shared node with no graph edges.
#[derive(Debug)]
pub struct Node {
    label: Box<str>,
}

impl Node {
    /// Allocates one shared node.
    pub fn shared(label: impl Into<Box<str>>) -> Rc<Self> {
        Rc::new(Self {
            label: label.into(),
        })
    }

    /// Borrows the node label.
    pub fn label(&self) -> &str {
        &self.label
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn baseline_clones_strong_ownership_only() {
        let root = Node::shared("root");
        let second_owner = Rc::clone(&root);
        assert_eq!(Rc::strong_count(&root), 2);
        assert_eq!(second_owner.label(), "root");
    }
}
