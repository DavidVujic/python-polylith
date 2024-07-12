from functools import reduce
from typing import Set

from polylith import alias
from polylith.distributions.core import (
    distributions_packages,
    distributions_sub_packages,
    get_distributions,
    get_packages_distributions,
)


def extract_extras(name: str) -> Set[str]:
    chars = ["[", "]"]
    replacement = ","

    res = reduce(lambda acc, char: str.replace(acc, char, replacement), chars, name)

    parts = str.split(res, replacement)

    return {str.strip(p) for p in parts if p}


def extract_library_names(deps: dict) -> Set[str]:
    names = {k for k, _v in deps["items"].items()}

    with_extras = [extract_extras(n) for n in names]

    return set().union(*with_extras)


def known_aliases_and_sub_dependencies(
    deps: dict, library_alias: list, options: dict
) -> Set[str]:
    """Collect known aliases (packages) for third-party libraries.

    When the library origin is not from a lock-file:
    collect sub-dependencies and distribution top-namespace for each library, and append to the result.
    """

    lock_file = any(str.endswith(deps["source"], s) for s in {".lock", ".txt"})
    third_party_libs = extract_library_names(deps)

    fn = options.get("dists_fn", get_distributions)
    dists = fn()

    dist_packages = distributions_packages(dists)
    custom_aliases = alias.parse(library_alias)
    sub_deps = distributions_sub_packages(dists) if not lock_file else {}

    a = alias.pick(dist_packages, third_party_libs)
    b = alias.pick(custom_aliases, third_party_libs)
    c = alias.pick(sub_deps, third_party_libs)
    d = get_packages_distributions(third_party_libs)

    return third_party_libs.union(a, b, c, d)
