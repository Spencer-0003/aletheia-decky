// SPDX-FileCopyrightText: 2026 Spencer
// SPDX-License-Identifier: AGPL-3.0-only

import { callable } from "@decky/api";

export type Settings = {
  auto_backup: boolean;
  auto_restore: boolean;
}

export const isInstalled = callable<[], boolean>('is_installed');
export const getSettings = callable<[], Settings>('get_settings');
export const setSetting = callable<[key: keyof Settings, value: boolean], Settings>('set_setting');
export const onLaunch = callable<[appId: string]>('on_launch');
export const onExit = callable<[appId: string]>('on_exit');