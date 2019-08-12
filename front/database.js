const fs = require('fs')
const path = require('path')
const initSqlJs = require('./sql-wasm')
const { ipcRenderer } = require('electron')

function first () {
  let exist = false

  if (fs.existsSync(path.join(__dirname, '../back/s3_1_beta.db'))) {
    exist = true
  }

  ipcRenderer.send('database-exist', exist)
}

function display (result) {
  var core = document.getElementById('core')
  var support = document.getElementById('support')

  var coreText = core.innerHTML + result.core
  var supporText = support.innerHTML + result.support

  if (result.core === 'TBD') {
    coreText = coreText + ', ' + result.coreremaining + ' games remaining.'
  }

  if (result.support === 'TBD') {
    supporText = supporText + ', ' + result.supportremaining + ' games remaining.'
  }

  core.innerHTML = coreText
  support.innerHTML = supporText
}

function read () {
  const filebuffer = fs.readFileSync(path.join(__dirname, '../back/s3_1_beta.db'))

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
