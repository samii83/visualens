# Renderer (React) — VisuaLens

This folder contains the React renderer used inside the Electron app.

Quick commands (within `electron-app`):
- `npm run dev` — start the renderer dev server (usually `vite`)
- `npm run build` — build the renderer assets

Key files:
- `src/index.jsx` — React DOM mounting point
- `src/App.jsx` — Root React component
- `src/api.js` — Wrapper for calling the backend
- `src/components` — UI components for Caption and Search
- `src/demo-data` — sample images and demo dataset for development
