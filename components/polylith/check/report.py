from polylith.check.core import run_command
from rich.console import Console
from rich.theme import Theme

info_theme = Theme(
    {
        "data": "#999966",
        "proj": "#8A2BE2",
        "comp": "#32CD32",
        "base": "#6495ED",
    }
)


def run(project_data: dict) -> bool:
    console = Console(theme=info_theme)

    project_name = project_data["name"]
    project_path = project_data["path"]

    with console.status(f"checking [proj]{project_name}[/]", spinner="monkey"):
        result = run_command(project_path)

        message = ["[proj]", project_name, "[/]", " "]
        extra = [":warning:"] if result else [":heavy_check_mark:"]

        output = "".join(message + extra)
        console.print(output)

        for row in result:
            console.print(f"[data]{row}[/]")

        return True if not result else False
