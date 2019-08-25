const { app, BrowserWindow, ipcMain, dialog } = require('electron')
const fs = require('fs')
const chokidar = require('chokidar')

// Create database directory if doesn't exists.
if (!fs.existsSync('../database')) {
  fs.mkdirSync('../database')
}

function dynamicPage (dbName) {
  if (fs.existsSync('../database/' + dbName)) {
    return 'index.html'
  } else {
    return 'welcome.html'
  }
}

function createWindow () {
  // Main window
  let main = new BrowserWindow({
    width: 600,
    height: 200,
    resizable: true,
    fullscreenable: false,
    show: false,
    webPreferences: {
      nodeIntegration: true
    }
  })

  const db = 'test.db'

  main.on('closed', () => {
    main = null
  })

  main.loadFile(dynamicPage(db))

  main.once('ready-to-show', () => {
    main.show()
  })

  ipcMain.on('select-file', (event) => {
    dialog.showOpenDialog(main, { properties: ['openFile'] }).then(result => {
      if (!result.canceled) {
        event.reply('file-selected', result.filePaths[0])
      }
    })
  })

  ipcMain.on('loaded', (event) => {
    main.loadFile(dynamicPage(db))
  })

  ipcMain.on('select-dir', (event) => {
    dialog.showOpenDialog(main, { properties: ['openDirectory'] }).then(result => {
      if (!result.canceled) {
        const watcher = chokidar.watch(result.filePaths[0], {
          ignoreInitial: true,
          persistent: true,
          depth: 0
        })

        watcher.on('add', path => {
          event.reply('new-file', path)
        })
      }
    })
  })
}

app.on('ready', createWindow)
