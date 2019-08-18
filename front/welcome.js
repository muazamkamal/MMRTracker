const { ipcRenderer } = require('electron')

function selectFile () {
  ipcRenderer.send('select-file')
}
