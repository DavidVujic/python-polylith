from pathlib import Path

from cleo.helpers import option
from poetry.console.commands.command import Command
from polylith import alias, check, info, project, repo, workspace
from polylith.poetry import internals

command_options = [
    option(
        long_name="strict",
        description="More strict checks when matching name of third-party libraries and imports",
        flag=True,
    ),
    option(
        long_name="alias",
        description="alias for a third-party library, useful when an import differ from the library name",
        flag=False,
        multiple=True,
    ),
]


class CheckCommand(Command):
    name = "poly check"
    description = "Validates the <comment>Polylith</> workspace."

    options = command_options

    def print_report(self, root: Path, ns: str, project_data: dict) -> bool:
        is_verbose = self.option("verbose")
        is_quiet = self.option("quiet")
        is_strict = self.option("strict")

        path = project_data["path"]
        name = project_data["name"]

        try:
            collected_imports = check.report.collect_all_imports(root, ns, project_data)
            third_party_libs = internals.find_third_party_libs(self.poetry, path)

            dists = internals.distributions(self.poetry, path)
            known_aliases = internals.distributions_packages(dists)
            known_aliases.update(alias.parse(self.option("alias")))

            extra = alias.pick(known_aliases, third_party_libs)

            libs = third_party_libs.union(extra)

            details = check.report.create_report(
                project_data,
                collected_imports,
                libs,
                is_strict,
            )

            res = all([not details["brick_diff"], not details["libs_diff"]])

            if is_quiet:
                return res

            check.report.print_missing_deps(details["brick_diff"], name)
            check.report.print_missing_deps(details["libs_diff"], name)

            if is_verbose:
                check.report.print_brick_imports(details["brick_imports"])
                check.report.print_brick_imports(details["third_party_imports"])

            return res
        except ValueError as e:
            self.line_error(f"{name}: <error>{e}</error>")
            return False

    def handle(self) -> int:
        root = repo.get_workspace_root(Path.cwd())
        ns = workspace.parser.get_namespace_from_config(root)

        all_projects_data = info.get_projects_data(root, ns)
        projects_data = [p for p in all_projects_data if info.is_project(p)]

        if self.option("directory"):
            project_name = project.get_project_name(self.poetry.pyproject.data)
            data = next((p for p in projects_data if p["name"] == project_name), None)

            if not data:
                raise ValueError(f"Didn't find project in {self.option('directory')}")

            res = self.print_report(root, ns, data)
            return 0 if res else 1

        results = {self.print_report(root, ns, data) for data in projects_data}

        return 0 if all(results) else 1
