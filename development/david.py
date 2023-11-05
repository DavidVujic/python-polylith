from pathlib import Path

from polylith import (
    bricks,
    development,
    diff,
    dirs,
    files,
    info,
    interface,
    poetry,
    poetry_plugin,
    project,
    readme,
    repo,
    test,
    workspace,
)

print("hello world")
print(repo.bases_dir)
print(repo.components_dir)
print(repo.projects_dir)

root = Path.cwd()
ns = workspace.parser.get_namespace_from_config(root)

tag = diff.collect.get_latest_tag(root, "release") or ""

changed_files = diff.collect.get_files(tag)
changed_components = diff.collect.get_changed_components(changed_files, ns)
changed_bases = diff.collect.get_changed_bases(changed_files, ns)
changed_projects = diff.collect.get_changed_projects(changed_files)

projects_data = info.get_bricks_in_projects(root, changed_components, changed_bases, ns)

bases_data = bricks.base.get_bases_data(root, ns)
