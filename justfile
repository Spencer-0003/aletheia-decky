# SPDX-FileCopyrightText: 2026 Spencer
# SPDX-License-Identifier: AGPL-3.0-only

build:
  mkdir build
  pnpm build
  mv dist build
  cp LICENSE build
  cp main.py build
  cp package.json build
  cp plugin.json build