const { app, BrowserWindow } = require('electron')
const fs = require('fs')

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

  if (fs.existsSync('../back/s3_1_beta.db')) {
    main.loadFile('index.html')
  } else {
    main.loadFile('first-setup.html')
  }

  main.once('ready-to-show', () => {
    main.show()
  })
}

app.on('ready', createWindow)
