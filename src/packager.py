import subprocess
from pathlib import Path
from typing import List


def build_exe(entry: Path, onefile: bool = True, extra_args: List[str] = None) -> int:
    cmd = ["pyinstaller"]
    if onefile:
        cmd.append("--onefile")
    cmd.append(str(entry))
    if extra_args:
        cmd.extend(extra_args)
    try:
        res = subprocess.run(cmd, check=False)
        return res.returncode
    except Exception:
        return 1
