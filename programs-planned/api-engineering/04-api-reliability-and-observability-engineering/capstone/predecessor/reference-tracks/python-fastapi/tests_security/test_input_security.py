import io
from pathlib import Path

import pytest

from api_security.errors import SecurityControlError
from api_security.input_security import ArchiveMember, confined_path, copy_bounded, reject_symlink, validate_archive_members, validate_filename


def test_shared_path_filename_archive_vectors(vector_loader):
    data = vector_loader("input-security.json")
    for case in data["pathCases"]:
        if case["valid"]:
            assert str(confined_path(Path(case["root"]), case["value"], percent_decode=case.get("decode", True))) == case["result"]
        else:
            with pytest.raises(SecurityControlError):
                confined_path(Path(case["root"]), case["value"], percent_decode=case.get("decode", True))
    for case in data["filenameCases"]:
        if case["valid"]:
            assert validate_filename(case["value"]) == case["value"]
        else:
            with pytest.raises(SecurityControlError):
                validate_filename(case["value"])
    for case in data["archiveCases"]:
        members=[ArchiveMember(x["name"],x["size"],x.get("kind","file")) for x in case["members"]]
        kwargs={k:v for k,v in {"max_members":case.get("maxMembers"),"max_total_bytes":case.get("maxTotal")}.items() if v is not None}
        if case["valid"]:
            validate_archive_members(members, **kwargs)
        else:
            with pytest.raises(SecurityControlError):
                validate_archive_members(members, **kwargs)


def test_bounded_copy_and_symlink(tmp_path):
    target=io.BytesIO()
    assert copy_bounded([b"abc",b"def"],target,max_bytes=6)==6
    with pytest.raises(SecurityControlError):
        copy_bounded([b"abc",b"def"],io.BytesIO(),max_bytes=5)
    outside=tmp_path.parent/"outside-fixture"
    outside.write_text("x")
    link=tmp_path/"link"
    link.symlink_to(outside)
    with pytest.raises(SecurityControlError):
        reject_symlink(link)
