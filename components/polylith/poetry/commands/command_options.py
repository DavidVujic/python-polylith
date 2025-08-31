from cleo.helpers import option

alias = option(
    long_name="alias",
    description="alias for a third-party library, useful when an import differ from the library name",
    flag=False,
    multiple=True,
)


save = option(
    long_name="save",
    description="Store the contents of this command to file",
    flag=True,
)


short = option(
    long_name="short",
    short_name="s",
    description="Print short view",
    flag=True,
)

since = option(
    long_name="since",
    description="Changed since a specific tag",
    flag=False,
)

strict = option(
    long_name="strict",
    description="More strict checks when matching name and version of third-party libraries and imports.",
    flag=True,
)
