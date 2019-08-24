const { PythonShell } = require('python-shell')
const { ipcRenderer } = require('electron')

function selectFile () {
  ipcRenderer.send('select-initial')
}

ipcRenderer.on('file-selected', (event, arg) => {
  // console.log(arg)

  const options = {
    mode: 'text',
    pythonPath: '../env/bin/python',
    pythonOptions: ['-u'], // get print results in real-time
    scriptPath: '../back',
    args: [arg, 'test']
  }

  PythonShell.run('front.py', options, function (err, results) {
    if (err) throw err

    ipcRenderer.send('loaded')
  })
})
