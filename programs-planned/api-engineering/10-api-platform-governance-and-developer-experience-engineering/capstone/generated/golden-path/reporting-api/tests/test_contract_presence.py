from pathlib import Path


def test_contract_stub_exists() -> None:
    assert Path("contracts/contract.stub").is_file()
