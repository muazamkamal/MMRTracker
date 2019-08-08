const { app, BrowserWindow } = require('electron')

let win

function createWindow()
{
    win = new BrowserWindow({
        width: 600,
        height: 200,
        resizable: true,
        fullscreenable: false,
        webPreferences: {
            nodeIntegration: true
        }
    })

    win.loadFile('index.html')

    win.on('closed', () => {
        win = null
    })
}

app.on('ready', createWindow)