const { app, BrowserWindow, ipcMain } = require('electron')

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

  main.on('closed', () => {
    main = null
  })

  // Loading window
  let loading = new BrowserWindow({
    width: 600,
    height: 200,
    resizable: true,
    fullscreenable: false,
    webPreferences: {
      nodeIntegration: true
    }
  })

  loading.loadFile('loading.html')
  // loading.webContents.openDevTools()

  loading.on('closed', () => {
    loading = null
  })

  ipcMain.once('database-exist', (event, status) => {
    if (status) {
      main.loadFile('index.html')
    } else {
      main.loadFile('first-setup.html')
    }

    loading.destroy()
    loading = null

    // main.webContents.openDevTools()
    main.once('ready-to-show', () => {
      main.show()
    })
  })
}

app.on('ready', createWindow)
