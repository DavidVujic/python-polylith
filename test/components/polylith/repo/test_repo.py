from polylith.repo import repo


def test_is_pep_621_ready():
    name = {"name": "hello world"}

    poetry_section = {"tool": {"poetry": name}}
    project_section = {"project": name}

    assert repo.is_pep_621_ready(poetry_section) is False
    assert repo.is_pep_621_ready(project_section) is True
