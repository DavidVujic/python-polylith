from typing import Set

from polylith import alias
from polylith.distributions.core import (
    distributions_packages,
    distributions_sub_packages,
    get_distributions,
    get_packages_distributions,
)


def known_aliases_and_sub_dependencies(deps: dict, library_alias: list) -> Set[str]:
    """Collect known aliases (packages) for third-party libraries.

    When the library origin is not from a lock-file:
    collect sub-dependencies and distribution top-namespace for each library, and append to the result.
    """

    lock_file = any(str.endswith(deps["source"], s) for s in {".lock", ".txt"})
    third_party_libs = {k for k, _v in deps["items"].items()}

    dists = get_distributions()

    dist_packages = distributions_packages(dists)
    custom_aliases = alias.parse(library_alias)
    sub_deps = distributions_sub_packages(dists) if not lock_file else {}

    a = alias.pick(dist_packages, third_party_libs)
    b = alias.pick(custom_aliases, third_party_libs)
    c = alias.pick(sub_deps, third_party_libs)

    d = get_packages_distributions(third_party_libs) if not lock_file else set()

    return third_party_libs.union(a, b, c, d)
