from pathlib import Path

from polylith import (
    alias,
    bricks,
    check,
    commands,
    configuration,
    development,
    diff,
    dirs,
    distributions,
    files,
    hatch,
    imports,
    info,
    interface,
    libs,
    parsing,
    pdm,
    poetry,
    project,
    readme,
    repo,
    reporting,
    sync,
    test,
    toml,
    workspace,
)

print("hello world")
print(repo.bases_dir)
print(repo.components_dir)
print(repo.projects_dir)

root = Path.cwd()
ns = configuration.get_namespace_from_config(root)

tag = diff.collect.get_latest_tag(root, "release") or ""

changed_files = diff.collect.get_files(tag)
changed_components = diff.collect.get_changed_components(root, changed_files, ns)
changed_bases = diff.collect.get_changed_bases(root, changed_files, ns)
changed_projects = diff.collect.get_changed_projects(root, changed_files)

projects_data = info.get_bricks_in_projects(root, changed_components, changed_bases, ns)

bases_data = bricks.base.get_bases_data(root, ns)
