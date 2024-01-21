from polylith.repo import repo


def test_is_pep_621_ready():
    poetry_section = {"build-system": {"build-backend": "poetry.core.masonry.api"}}
    project_section = {"project": {"name": "hello world"}}
    both = {**poetry_section, **project_section}

    assert repo.is_pep_621_ready(poetry_section) is False
    assert repo.is_pep_621_ready(project_section) is True

    assert repo.is_pep_621_ready(both) is False
