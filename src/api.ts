// SPDX-FileCopyrightText: 2026 Spencer
// SPDX-License-Identifier: AGPL-3.0-only

import { callable } from "@decky/api";

export const onLaunch = callable<[appId: string]>('on_launch');
export const onExit = callable<[appId: string]>('on_exit');