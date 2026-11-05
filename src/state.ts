// SPDX-FileCopyrightText: 2026 Spencer
// SPDX-License-Identifier: AGPL-3.0-only

import { useEffect, useState } from 'react';

const listeners = new Set<(busy: boolean) => void>();
let busy = false;

export function setBusy(value: boolean) {
  busy = value;
  listeners.forEach(l => l(value));
}

export function useBusy(): boolean {
  const [value, setValue] = useState(busy);

  useEffect(() => {
    listeners.add(setValue);
    setValue(busy);

    return () => {
      listeners.delete(setValue);
    }
  }, []);

  return value;
}