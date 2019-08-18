const { ipcRenderer } = require('electron')

function selectFile () {
  ipcRenderer.send('select-file')
}

ipcRenderer.on('file-selected', (event, arg) => {
  console.log(arg)
})
