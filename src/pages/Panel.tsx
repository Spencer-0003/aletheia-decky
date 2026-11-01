// SPDX-FileCopyrightText: 2026 Spencer
// SPDX-License-Identifier: AGPL-3.0-only

import { ButtonItem, PanelSection, PanelSectionRow, ToggleField } from '@decky/ui';
import { useState } from 'react';

export function Panel() {
  const [busy, setBusy] = useState(false);

  return (
    <>
      <PanelSection title='Automation'>
        <PanelSectionRow>
          <ToggleField
            label='Back up when a game exits'
            checked={false}
          />
        </PanelSectionRow>
        <PanelSectionRow>
          <ToggleField
            label='Restore when a game launches'
            checked={false}
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