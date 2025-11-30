// electron-app/src/main/preload.js
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  getApiConfig: () => ipcRenderer.invoke('get-api-config'),
  // You can expose other backend-related functions here
});
