// SPDX-FileCopyrightText: 2026 Spencer
// SPDX-License-Identifier: AGPL-3.0-only

import { toaster } from '@decky/api';
import { getSettings, isInstalled, setSetting, type Settings } from '../api';
import { ButtonItem, PanelSection, PanelSectionRow, ToggleField } from '@decky/ui';
import { useEffect, useState } from 'react';

export function Panel() {
  const [busy, setBusy] = useState(false);
  const [installed, setInstalled] = useState(false);
  const [settings, setSettings] = useState<Settings | null>(null);

  useEffect(() => {
    let cancelled = false;

    isInstalled()
      .then(v => {
        if (!cancelled) setInstalled(v);
      });

    getSettings()
      .then(s => {
        if (!cancelled) setSettings(s);
      });

    return () => {
      cancelled = true;
    }
  }, []);

  const update = async (key: keyof Settings, value: boolean) => {
    setSettings(current => (current ? { ...current, [key]: value } : current));

    try {
      setSettings(await setSetting(key, value))
    } catch (e) {
      setSettings(current => (current ? { ...current, [key]: !value } : current));
      toaster.toast({ title: 'Error', body: 'Failed to save configuration.' });
    }
  }

  if (!installed) return (
    <PanelSection>
      <PanelSectionRow>Aletheia is not installed. Install it, then reload the plugin,</PanelSectionRow>
    </PanelSection>
  );

  return (
    <>
      <PanelSection title='Automation'>
        <PanelSectionRow>
          <ToggleField
            label='Back up when a game exits'
            checked={settings?.auto_backup ?? false}
            disabled={!settings}
            onChange={v => update('auto_backup', v)}
          />
        </PanelSectionRow>
        <PanelSectionRow>
          <ToggleField
            label='Restore when a game launches'
            checked={settings?.auto_restore ?? false}
            disabled={!settings}
            onChange={v => update('auto_restore', v)}
          />
        </PanelSectionRow>
        <PanelSectionRow>
          <ButtonItem layout='below' disabled={busy}>
            {busy ? 'Backing up…' : 'Back up all games'}
          </ButtonItem>
        </PanelSectionRow>
      </PanelSection>
    </>
  )
}