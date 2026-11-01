# SPDX-FileCopyrightText: 2026 Spencer
# SPDX-License-Identifier: AGPL-3.0-only

import decky

TOAST_EVENT = 'aletheia.toast'

async def notify(title: str, body: str) -> None:
    await decky.emit(TOAST_EVENT, title, body)

class Plugin:
    async def on_launch(self, appId: str):
        await notify('Game started', appId)

    async def on_exit(self, appId: str):
        await notify('Game exited', appId)