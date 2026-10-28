#![forbid(unsafe_code)]

use std::rc::Rc;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Node {
    title: String,
    children: Vec<Rc<Node>>,
}

impl Node {
    pub fn new(title: impl Into<String>, children: Vec<Rc<Node>>) -> Rc<Self> {
        Rc::new(Self {
            title: title.into(),
            children,
        })
    }

    pub fn title(&self) -> &str {
        &self.title
    }

    pub fn children(&self) -> &[Rc<Node>] {
        &self.children
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum PathError {
    MissingChild { depth: usize, index: usize },
}

#[cfg(test)]
mod tests {
    use super::Node;
    use std::rc::Rc;

    #[test]
    fn starter_can_share_an_immutable_child() {
        let child = Node::new("child", vec![]);
        let first = Node::new("first", vec![Rc::clone(&child)]);
        let second = Node::new("second", vec![Rc::clone(&child)]);
        assert!(Rc::ptr_eq(&first.children()[0], &second.children()[0]));
    }
}
