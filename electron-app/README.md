# Electron App — VisuaLens

This folder contains the Electron + React frontend for VisuaLens.

Quick commands:
- `npm install` — install renderer & electron dependencies
- `npm run dev` — start the renderer dev server and Electron in dev mode (setup depends on electron-vite config)
- `npm run build` — bundle renderer and package Electron app

Notes for developers:
- The renderer files live under `src/renderer/src/` and the Electron main process files are in `src/main/`.
- The `src/demo-data/` folder contains sample images for offline development.
- Use `src/renderer/src/api.js` to make calls to the backend (default `http://localhost:8000`).
