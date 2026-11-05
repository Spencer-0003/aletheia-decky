# SPDX-FileCopyrightText: 2026 Spencer
# SPDX-License-Identifier: AGPL-3.0-only

import asyncio
import contextlib
import os
import shlex
import shutil
import signal
import subprocess

FLATPAK_ID = 'moe.spencer.Aletheia'

class Engine:
    def __init__(self):
        self.command = self._find_command()

    def _find_command(self) -> str | None:
        native = shutil.which('aletheia')
        if native is not None:
            return native

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

    async def _run(self, *args: str, timeout: float) -> int:
        process = await asyncio.create_subprocess_exec(
            *shlex.split(self.command),
            *args,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL,
            start_new_session=True
        )

        try:
            return await asyncio.wait_for(process.wait(), timeout)
        except asyncio.TimeoutError:
            with contextlib.suppress(ProcessLookupError):
                os.killpg(process.pid, signal.SIGKILL)
            await process.wait()
            raise

    async def is_installed(self) -> bool:
        return self.command is not None

    async def backup_all(self) -> str | None:
        try:
            code = await self._run('backup', timeout=10)
        except:
            return 'Aletheia took too long and was stopped'

        return None if code == 0 else f'Aletheia exited with code {code}'

    async def on_launch(self, app_id: str):
        pass

    async def on_exit(self, app_id: str):
        pass