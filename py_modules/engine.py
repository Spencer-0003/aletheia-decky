# SPDX-FileCopyrightText: 2026 Spencer
# SPDX-License-Identifier: AGPL-3.0-only

from pathlib import Path
import shlex
import shutil
import subprocess

FLATPAK_ID = 'moe.spencer.Aletheia'
NATIVE_PATH = Path('/usr/bin/aletheia')

class Engine:
    def __init__(self):
        self.command = self._find_command()

    def _find_command(self) -> str | None:
        if NATIVE_PATH.is_file():
            return str(NATIVE_PATH)

        flatpak = shutil.which('flatpak')
        if flatpak is None:
            return None

        try:
            result = subprocess.run(
                [flatpak, 'info', FLATPAK_ID],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=5
            )
        except (OSError, subprocess.TimeoutExpired):
            return None

        return shlex.join([flatpak, 'run', FLATPAK_ID]) if result.returncode == 0 else None

    async def is_installed(self) -> bool:
        return self.command is not None

    async def on_launch(self, app_id: str):
        pass

    async def on_exit(self, app_id: str):
        pass