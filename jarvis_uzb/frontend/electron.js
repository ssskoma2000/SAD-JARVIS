const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const isDev = !app.isPackaged;

// 3D modelning to'liq yo'lini olish
const modelPath = path.join(app.getAppPath(), '../../ironman/iron_man_mark_ix__marvel_fan_art.glb');


function createWindow() {
  const win = new BrowserWindow({
    width: 400,
    height: 400,
    transparent: true,
    frame: false,
    alwaysOnTop: true,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
    },
  });
  
  // Model yo'lini so'rash uchun handler
  ipcMain.handle('get-model-path', () => modelPath);

  // Oynani harakatlantirish uchun mantiq
  let drag = { isDragging: false, startX: 0, startY: 0, winX: 0, winY: 0 };
  
  ipcMain.on('drag-start', (event, { clientX, clientY }) => {
    drag.isDragging = true;
    [drag.winX, drag.winY] = win.getPosition();
    drag.startX = clientX;
    drag.startY = clientY;
  });

  ipcMain.on('dragging', (event, { clientX, clientY }) => {
    if (drag.isDragging) {
      const offsetX = clientX - drag.startX;
      const offsetY = clientY - drag.startY;
      win.setPosition(drag.winX + offsetX, drag.winY + offsetY);
    }
  });

  ipcMain.on('drag-end', () => {
    drag.isDragging = false;
  });

  const url = isDev
    ? 'http://localhost:5173'
    : `file://${path.join(__dirname, 'dist', 'index.html')}`;
  
  win.loadURL(url);

  if (isDev) {
    win.webContents.openDevTools({ mode: 'detach' });
  }
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});