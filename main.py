# SPDX-FileCopyrightText: 2026 Spencer
# SPDX-License-Identifier: AGPL-3.0-only

from pathlib import Path

import decky
from config import SettingsStore

TOAST_EVENT = 'aletheia.toast'

async def notify(title: str, body: str) -> None:
    await decky.emit(TOAST_EVENT, title, body)

class Plugin:
    settings: SettingsStore

    async def _main(self):
        self.settings = SettingsStore(Path(decky.DECKY_PLUGIN_SETTINGS_DIR) / 'settings.json')

    async def get_settings(self) -> dict[str, bool]:
        return self.settings.all()

    async def set_setting(self, key: str, value: bool) -> dict[str, bool]:
        self.settings.set(key, value)
        return self.settings.all()

    async def on_launch(self, appId: str):
        await notify('Game started', appId)

    async def on_exit(self, appId: str):
        await notify('Game exited', appId)