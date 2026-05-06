/**
 * preload.js — Secure bridge between Electron and React.
 * Exposes only specific APIs to the renderer (React app).
 */
const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("electronAPI", {
  // Window controls (used by the custom title bar)
  minimize: () => ipcRenderer.send("window-minimize"),
  maximize: () => ipcRenderer.send("window-maximize"),
  close:    () => ipcRenderer.send("window-close"),

  // Check if running inside Electron
  isElectron: true,
});