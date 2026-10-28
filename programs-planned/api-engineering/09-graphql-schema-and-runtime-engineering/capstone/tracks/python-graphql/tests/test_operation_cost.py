import unittest
from graph_api.cost import CostPolicy, analyze
from graph_api.model import ValidationError
from graph_api.operation import parse_document

class OperationCostTests(unittest.TestCase):
    def test_parses_fragments_aliases_and_inline_fragments(self):
        doc=parse_document('query Q { a: project(id:"1") { ...P } } fragment P on Project { id ... on Project { name } }')
        report=analyze(doc,operation_name="Q"); self.assertEqual(report.aliases,1); self.assertGreaterEqual(report.depth,2)
    def test_fragment_cycle_rejected(self):
        doc=parse_document('query Q { project(id:"1") { ...A } } fragment A on Project { ...B } fragment B on Project { ...A }')
        with self.assertRaises(ValidationError): analyze(doc,operation_name="Q")
    def test_alias_budget(self):
        fields=' '.join(f'a{i}: viewer {{ subject }}' for i in range(4)); doc=parse_document(f'query Q {{ {fields} }}')
        with self.assertRaises(ValidationError): analyze(doc,operation_name="Q",policy=CostPolicy(max_aliases=3))
    def test_page_size_bound(self):
        doc=parse_document('query Q($first:Int!){ analysisRuns(first:$first){ edges { node { id } } } }')
        with self.assertRaises(ValidationError): analyze(doc,operation_name="Q",variables={"first":101})
