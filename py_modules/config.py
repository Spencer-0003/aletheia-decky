# SPDX-FileCopyrightText: 2026 Spencer
# SPDX-License-Identifier: AGPL-3.0-only

from pathlib import Path
import json

DEFAULTS = {
    'auto_backup': True,
    'auto_restore': False
}

class SettingsStore:
    def __init__(self, path: Path):
        self._data: dict = {}
        self._path = path

        try:
            self._data = json.loads(self._path.read_text(encoding='utf-8'))
        except FileNotFoundError:
            return
        except (OSError, ValueError):
            return # TODO: Send notification to frontend

    def get(self, key: str) -> bool:
        return self._data.get(key)

    def all(self) -> dict[str, bool]:
        return { key: self.get(key) for key in DEFAULTS }

    def set(self, key: str, value: bool) -> None:
        updated = { **self._data, key: value }
        self._save(updated)
        self._data = updated

    def _save(self, data: dict) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(json.dumps(data, indent=2), encoding='utf-8')