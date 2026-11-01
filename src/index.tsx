// SPDX-FileCopyrightText: 2026 Spencer
// SPDX-License-Identifier: AGPL-3.0-only

import { staticClasses } from '@decky/ui';
import { addEventListener, definePlugin, removeEventListener, toaster } from '@decky/api';
import { FaSave } from 'react-icons/fa';
import { Panel } from './pages/Panel';
import { onExit, onLaunch } from './api';

const TOAST_EVENT = 'aletheia.toast';

export default definePlugin(() => {
  const onToast = (title: string, body: string) => toaster.toast({ title, body });

  addEventListener(TOAST_EVENT, onToast);

  const launchHook = SteamClient.Apps.RegisterForGameActionStart((_actionId, appId, action) => {
    if (action == 'launchApp') onLaunch(appId);
  });

  const exitHook = SteamClient.GameSessions.RegisterForAppLifetimeNotifications(notification => {
    if (!notification.bRunning) onExit(notification.unAppID.toString());
  });

  return {
    name: 'Aletheia',
    titleView: <div className={staticClasses.Title}>Aletheia</div>,
    icon: <FaSave />,
    content: <Panel />,
    onDismount() {
      launchHook.unregister();
      exitHook.unregister();
      removeEventListener(TOAST_EVENT, onToast);
    }
  };
});