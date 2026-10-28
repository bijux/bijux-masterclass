//! Acyclic shared tree with weak parent backlinks.
use std::fmt;
use std::rc::{
    Rc, Weak
};
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct NodeId(pub u64);
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct NodeSpec {
    pub id: NodeId,
    pub label: String,
    pub children: Vec<NodeSpec>,
}
#[derive(Debug)]
pub struct Node {
    id: NodeId,
    label: Box<str>,
    parent: Weak<Node>,
    children: Vec<Rc<Node>>,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BuildError {
    DuplicateId(NodeId)
}
impl fmt::Display for BuildError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::DuplicateId(id) => write!(f, "duplicate node id {}", id.0)
        }
    }
}
impl std::error::Error for BuildError {
}
impl Node {
    pub fn build(spec: NodeSpec) -> Result<Rc<Self>, BuildError> {
        let mut ids = std::collections::HashSet::new();
        validate_ids(&spec, &mut ids)?;
        Ok(build_node(spec, Weak::new()))
    }
    pub fn id(&self) -> NodeId {
        self.id
    }
    pub fn label(&self) -> &str {
        &self.label
    }
    pub fn children(&self) -> &[Rc<Node>] {
        &self.children
    }
    pub fn parent(&self) -> Option<Rc<Node>> {
        self.parent.upgrade()
    }
    pub fn find(root: &Rc<Node>, id: NodeId) -> Option<Rc<Node>> {
        if root.id == id {
            return Some(Rc::clone(root));
        }
        root.children.iter().find_map(|child| Self::find(child, id))
    }
    pub fn path_to_root(node: &Rc<Node>) -> Vec<NodeId> {
        let mut path = Vec::new();
        let mut current = Some(Rc::clone(node));
        while let Some(node) = current {
            path.push(node.id);
            current = node.parent();
        }
        path
    }
}
fn validate_ids(spec: &NodeSpec, ids: &mut std::collections::HashSet<NodeId>) -> Result<(), BuildError> {
    if !ids.insert(spec.id) {
        return Err(BuildError::DuplicateId(spec.id));
    }
    for child in &spec.children {
        validate_ids(child, ids)?;
    }
    Ok(())
}
fn build_node(spec: NodeSpec, parent: Weak<Node>) -> Rc<Node> {
    Rc::new_cyclic(|weak_self| {
        let children = spec.children.into_iter().map(|child| build_node(child, weak_self.clone())).collect();
        Node {
            id: spec.id, label: spec.label.into_boxed_str(), parent, children
        }
    })
}
#[cfg(test)]
mod tests {
    use super::*;
    fn tree() -> Rc<Node> {
        match Node::build(NodeSpec {
            id: NodeId(1), label: "root".into(), children: vec![NodeSpec {
                id: NodeId(2), label: "child".into(), children: vec![]
            }]
        }) {
            Ok(value) => value, Err(error) => panic!("{error}"),
        }
    }
    #[test]
    fn parent_is_weak_and_navigation_works() {
        let root = tree();
        let child = match Node::find(&root, NodeId(2)) {
            Some(v) => v, None => panic!("missing")
        };
        assert_eq!(Node::path_to_root(&child), [NodeId(2), NodeId(1)]);
        assert!(Rc::ptr_eq(&child.parent().unwrap_or_else(|| panic!("missing parent")), &root));
    }
    #[test]
    fn component_reclaims_after_roots_drop() {
        let root = tree();
        let child = Node::find(&root, NodeId(2)).unwrap_or_else(|| panic!("missing"));
        let root_probe = Rc::downgrade(&root);
        let child_probe = Rc::downgrade(&child);
        drop(child);
        drop(root);
        assert!(root_probe.upgrade().is_none());
        assert!(child_probe.upgrade().is_none());
    }
    #[test]
    fn rejects_duplicate_domain_identity() {
        let result = Node::build(NodeSpec {
            id: NodeId(1), label: "a".into(), children: vec![NodeSpec {
                id: NodeId(1), label: "b".into(), children: vec![]
            }]
        });
        assert!(matches!(result, Err(BuildError::DuplicateId(NodeId(1)))));
    }
}
