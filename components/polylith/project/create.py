from pathlib import Path
from typing import List

import tomlkit
from polylith import repo, sync
from polylith.dirs import create_dir
from polylith.repo import projects_dir
from polylith.reporting import theme
from rich.console import Console
from rich.prompt import Prompt


def create_project_toml(template: str, template_data: dict) -> tomlkit.TOMLDocument:
    content = template.format(**template_data)

    return tomlkit.loads(content)


def create_project(path: Path, template: str, name: str, description: str) -> None:
    d = create_dir(path, f"{projects_dir}/{name}")

    authors = repo.get_authors(path)
    python_version = repo.get_python_version(path)

    description_field = f'description = "{description}"' if description else ""
    authors_field = f"authors = {authors}" if authors else ""

    project_toml = create_project_toml(
        template,
        {
            "name": name,
            "description": description_field,
            "authors": authors_field,
            "python_version": python_version,
        },
    )

    fullpath = d / repo.default_toml

    with fullpath.open("w", encoding="utf-8") as f:
        f.write(tomlkit.dumps(project_toml))


def interactive_add_bricks_to_project(
    root: Path,
    ns: str,
    project_name: str,
    possible_bases: List[str],
) -> None:
    console = Console(theme=theme.poly_theme)
    first, *_ = possible_bases

    question = f"[data]What's the name of the Polylith [base]base[/] to add to the [proj]{project_name}[/] project?[/]"
    console.print(question)

    base = Prompt.ask(
        prompt="[data]Base[/]",
        console=console,
        default=first,
        show_default=True,
        case_sensitive=False,
    )

    res = sync.collect.calculate_needed_bricks(root, ns, base)

    print(res)
