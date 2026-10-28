from __future__ import annotations
import json
from pathlib import Path

COURSE=Path(__file__).resolve().parents[1]

def test_course_metadata() -> None:
    value=json.loads((COURSE/"course.json").read_text())
    assert value["courseNumber"]==3
    assert value["id"]=="container-oci-and-software-supply-chain-engineering"
    assert value["primaryProduct"]=="course-book"
