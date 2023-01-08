import os
import subprocess
from pathlib import Path
from typing import List


def navigate_to(path: Path):
    os.chdir(str(path))


def run_command(project_path: Path) -> List[str]:
    current_dir = Path.cwd()

    navigate_to(project_path)

    try:
        res = subprocess.run(
            ["poetry", "check-project"], capture_output=True, text=True
        )
    finally:
        navigate_to(current_dir)

    res.check_returncode()

    return res.stdout.splitlines()
