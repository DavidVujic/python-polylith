import os
import subprocess
from pathlib import Path
from typing import List


def navigate_to(path: Path):
    os.chdir(str(path))


def run_command(project_path: Path) -> List[str]:
    current_dir = Path.cwd()

    navigate_to(project_path)

    res = subprocess.run(["which", "poetry"], capture_output=True, text=True)
    print(res)
    navigate_to(current_dir)

    return res.stdout.splitlines()
