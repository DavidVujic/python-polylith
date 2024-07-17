from typer import Option

alias = Option(
    help="alias for third-party libraries, useful when an import differ from the library name"
)
directory = Option(
    help="The working directory for the command (defaults to the current working directory)."
)

short = Option(help="Print short view.")
short_workspace = Option(help="Display Workspace Info adjusted for many projects.")

strict = Option(
    help="More strict checks when matching name and version of third-party libraries and imports."
)

verbose = Option(help="More verbose output.")
quiet = Option(help="Do not output any messages.")

brick = Option(help="Shows dependencies for selected brick.")
