const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  getModelPath: () => ipcRenderer.invoke('get-model-path'),
  
  // Oyna harakati uchun
  dragStart: (e) => ipcRenderer.send('drag-start', { clientX: e.clientX, clientY: e.clientY }),
  dragging: (e) => ipcRenderer.send('dragging', { clientX: e.clientX, clientY: e.clientY }),
  dragEnd: () => ipcRenderer.send('drag-end'),
});