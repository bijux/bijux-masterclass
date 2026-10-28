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

pub fn rename_at_path(
    root: &Rc<Node>,
    path: &[usize],
    title: impl Into<String>,
) -> Result<Rc<Node>, PathError> {
    fn rebuild(
        node: &Rc<Node>,
        path: &[usize],
        depth: usize,
        title: &str,
    ) -> Result<Rc<Node>, PathError> {
        if path.is_empty() {
            return Ok(Node::new(title, node.children.clone()));
        }
        let index = path[0];
        if index >= node.children.len() {
            return Err(PathError::MissingChild { depth, index });
        }
        let mut children = node.children.clone();
        children[index] = rebuild(&children[index], &path[1..], depth + 1, title)?;
        Ok(Node::new(node.title.clone(), children))
    }

    let title = title.into();
    rebuild(root, path, 0, &title)
}

pub fn insert_at_path(
    root: &Rc<Node>,
    path: &[usize],
    child: Rc<Node>,
) -> Result<Rc<Node>, PathError> {
    fn rebuild(
        node: &Rc<Node>,
        path: &[usize],
        depth: usize,
        child: &Rc<Node>,
    ) -> Result<Rc<Node>, PathError> {
        if path.is_empty() {
            let mut children = node.children.clone();
            children.push(Rc::clone(child));
            return Ok(Node::new(node.title.clone(), children));
        }
        let index = path[0];
        if index >= node.children.len() {
            return Err(PathError::MissingChild { depth, index });
        }
        let mut children = node.children.clone();
        children[index] = rebuild(&children[index], &path[1..], depth + 1, child)?;
        Ok(Node::new(node.title.clone(), children))
    }

    rebuild(root, path, 0, &child)
}

pub fn titles_depth_first(root: &Node) -> Vec<&str> {
    let mut output = Vec::new();
    let mut stack = vec![root];
    while let Some(node) = stack.pop() {
        output.push(node.title());
        stack.extend(node.children.iter().rev().map(Rc::as_ref));
    }
    output
}

#[cfg(test)]
mod tests {
    use super::{Node, PathError, insert_at_path, rename_at_path, titles_depth_first};
    use std::rc::Rc;

    #[test]
    fn path_copy_preserves_old_root_and_shares_unchanged_subtree() {
        let first = Node::new("a", vec![]);
        let second = Node::new("b", vec![]);
        let root = Node::new("root", vec![Rc::clone(&first), Rc::clone(&second)]);
        let changed = rename_at_path(&root, &[0], "A").unwrap();

        assert_eq!(titles_depth_first(&root), vec!["root", "a", "b"]);
        assert_eq!(titles_depth_first(&changed), vec!["root", "A", "b"]);
        assert!(Rc::ptr_eq(&root.children()[1], &changed.children()[1]));
        assert!(!Rc::ptr_eq(&root, &changed));
    }

    #[test]
    fn invalid_path_returns_error_without_modifying_old_value() {
        let root = Node::new("root", vec![]);
        assert_eq!(
            rename_at_path(&root, &[0], "x"),
            Err(PathError::MissingChild { depth: 0, index: 0 })
        );
        assert_eq!(root.title(), "root");
    }

    #[test]
    fn insertion_path_copies_only_the_ancestor_spine() {
        let shared = Node::new("shared", vec![]);
        let root = Node::new("root", vec![Rc::clone(&shared)]);
        let next = insert_at_path(&root, &[], Node::new("child", vec![])).unwrap();
        assert_eq!(titles_depth_first(&next), vec!["root", "shared", "child"]);
        assert!(Rc::ptr_eq(&root.children()[0], &next.children()[0]));
    }
}
