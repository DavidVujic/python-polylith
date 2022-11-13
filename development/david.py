from pathlib import Path

from polylith import (
    bricks,
    development,
    diff,
    dirs,
    files,
    info,
    interface,
    log,
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

tag = diff.collect.get_latest_tag(root)

if tag:
    res = diff.collect.get_files(tag)
    print(diff.collect.get_changed_components(root, res))
    print(diff.collect.get_changed_bases(root, res))
    print(diff.collect.get_changed_projects(res))

info.get_bricks_in_projects(root)

ns = workspace.parser.get_namespace_from_config(root)
bases_data = bricks.base.get_bases_data(root, ns)
