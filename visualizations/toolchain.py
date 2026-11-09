"""The pinned compiler and debugger, and the error every rejected snippet raises."""
from __future__ import annotations

import os
import shutil
import subprocess


class Unsupported(ValueError):
    """The snippet cannot safely be represented by this visualization category."""


def run(command: list[str], *, timeout: int = 30) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(command, capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise Unsupported(f"tool execution failed: {exc}") from exc


def tool(env: str, executable: str) -> str:
    """The executable named by `env`, or found on PATH; both dev shells set the variables."""
    selected = os.environ.get(env) or shutil.which(executable)
    if not selected:
        raise Unsupported(f"{executable} is required (set {env})")
    return selected
