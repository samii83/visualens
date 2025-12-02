# electron-app/start-dev.ps1
# Convenience script to start the Electron app in dev mode.
# This will not start the Python backend; run backend/start-dev.ps1 in a separate terminal before starting this.

npm install
npm run dev
