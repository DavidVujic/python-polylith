from polylith.repo import repo


def test_is_pep_621_compliant():
    assert repo.is_pep_621_compliant({"tool": {"poetry": {}}}) is False
    assert repo.is_pep_621_compliant({"project": {"hello": "world"}}) is True
