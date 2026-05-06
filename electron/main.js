const { app, BrowserWindow, Tray, Menu, nativeImage, ipcMain } = require("electron");
const path = require("path");

const FRONTEND_URL = "http://localhost:3000";
const PRELOAD_PATH = path.join(__dirname, "preload.js");

let mainWindow = null;
let tray       = null;

// ── Main window ───────────────────────────────────────────────────────────────
function createWindow() {
  mainWindow = new BrowserWindow({
    width:           1280,
    height:          800,
    minWidth:        900,
    minHeight:       600,
    frame:           false,
    transparent:     true,
    backgroundColor: "#02040a",
    titleBarStyle:   "hidden",
    webPreferences: {
      preload:          PRELOAD_PATH,
      contextIsolation: true,
      nodeIntegration:  false,
    },
  });

  // Retry until React dev server is ready
  const tryLoad = (attempts = 0) => {
    mainWindow.loadURL(FRONTEND_URL).catch(() => {
      if (attempts < 30) {
        console.log(`Waiting for React dev server... (${attempts + 1}/30)`);
        setTimeout(() => tryLoad(attempts + 1), 1500);
      } else {
        console.error("Could not reach React dev server at", FRONTEND_URL);
      }
    });
  };
  tryLoad();

  // Ctrl+Shift+I → DevTools
  mainWindow.webContents.on("before-input-event", (_, input) => {
    if (input.control && input.shift && input.key === "I") {
      mainWindow.webContents.openDevTools();
    }
  });

  mainWindow.on("closed", () => { mainWindow = null; });
}

// ── System Tray ───────────────────────────────────────────────────────────────
function createTray() {
  tray = new Tray(nativeImage.createEmpty());
  tray.setToolTip("S.G.A — Your Personal AI");

  const menu = Menu.buildFromTemplate([
    { label: "Show S.G.A", click: () => { mainWindow ? mainWindow.show() : createWindow(); } },
    { label: "Hide",       click: () => mainWindow?.hide() },
    { type:  "separator" },
    { label: "Quit S.G.A", click: () => { app.isQuiting = true; app.quit(); } },
  ]);

  tray.setContextMenu(menu);
  tray.on("double-click", () => { mainWindow ? mainWindow.show() : createWindow(); });
}

// ── IPC: custom title bar controls ───────────────────────────────────────────
ipcMain.on("window-minimize", () => mainWindow?.minimize());
ipcMain.on("window-maximize", () => {
  mainWindow?.isMaximized() ? mainWindow.unmaximize() : mainWindow?.maximize();
});
ipcMain.on("window-close", () => mainWindow?.hide());  // hides to tray

// ── App lifecycle ─────────────────────────────────────────────────────────────
app.whenReady().then(() => {
  createWindow();
  createTray();
  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

// Stay running in tray when all windows closed
app.on("window-all-closed", (e) => {
  if (process.platform !== "darwin") e.preventDefault();
});