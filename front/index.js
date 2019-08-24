const fs = require('fs')
const initSqlJs = require('./sql-wasm')
const { ipcRenderer } = require('electron')
const { PythonShell } = require('python-shell')

function mmrToHTML (inMMR, remaining, delta) {
  var mmr = inMMR

  if (inMMR === 'TBD') {
    mmr += '<br>' + remaining + ' games remaining'
  } else {
    if (delta !== 0) {
      // TO-DO: Check negative or positive
      mmr += '<br>' + delta
    }
  }

  return mmr
}

function display (result) {
  var core = document.querySelector('#core-mmr')
  var support = document.querySelector('#support-mmr')

  // Core MMR
  core.innerHTML = mmrToHTML(result.core, result.coreremaining, result.coredelta)

  // Support MMR
  support.innerHTML = mmrToHTML(result.support, result.supportremaining, result.supportdelta)
}

function getLatest (dbName) {
  const filebuffer = fs.readFileSync('../database/' + dbName)

  initSqlJs().then(SQL => {
    // Create a database
    var db = new SQL.Database(filebuffer)
    // NOTE: You can also use new SQL.Database(data) where
    // data is an Uint8Array representing an SQLite database file

    // Prepare an sql statement
    db.each('SELECT * FROM mmr ORDER BY time DESC LIMIT 1', (row) => {
      display(row)
    })

    db.close()
  })
}

getLatest('test.db')

function updateMMR () {
  ipcRenderer.send('select-file')
}

ipcRenderer.on('file-selected', (event, arg) => {
  const options = {
    mode: 'text',
    pythonPath: '../env/bin/python',
    pythonOptions: ['-u'], // get print results in real-time
    scriptPath: '../back',
    args: [arg, 'test']
  }

  PythonShell.run('front.py', options, function (err, results) {
    if (err) throw err

    getLatest('test.db')
  })
})
