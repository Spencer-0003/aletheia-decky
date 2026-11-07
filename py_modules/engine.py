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

    async def _run(self, *args: str, timeout: float, env: dict[str, str] | None) -> int:
        argv = shlex.split(self.command)

        if env and os.path.basename(argv[0]) == 'flatpak':
            argv[2:2] = [f'--env={key}={value}' for key, value in env.items()]

        process = await asyncio.create_subprocess_exec(
            *argv,
            *args,
            env={**os.environ, **(env or {})},
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

    async def _action(self, command: str, *args: str, timeout: float, env: dict[str, str] | None = None) -> str | None:
        try:
            code = await self._run(command, *args, timeout=timeout, env=env)
        except:
            return 'Aletheia took too long and was stopped'

        return None if code == 0 else f'Aletheia exited with code {code}'

    async def backup_all(self) -> str | None:
        return await self._action('backup', timeout=10)

    async def backup_game(self, app_id: str) -> str | None:
        # Aletheia doesn't support passing steam IDs to the backup command so this is a hacky workaround
        return await self._action('backup', '--infer', 'steam', timeout=5, env={'SteamAppId': app_id})

    async def restore_game(self, app_id: str) -> str | None:
        # Same workaround for restore
        return await self._action('restore', '--infer', 'steam', timeout=5, env={'SteamAppId': app_id})

    async def on_launch(self, app_id: str):
        return await self.restore_game(app_id)

    async def on_exit(self, app_id: str):
        return await self.backup_game(app_id)