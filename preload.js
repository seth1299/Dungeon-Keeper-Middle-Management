const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('dkmm', {
  loadJSON: async (relativePath) => {
    if (typeof relativePath !== 'string') return null;
    return ipcRenderer.invoke('load-json', relativePath);
  }
});
