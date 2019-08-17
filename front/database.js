const fs = require('fs')
const initSqlJs = require('./sql-wasm')

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

function getLatest () {
  const filebuffer = fs.readFileSync('../back/s3_1_beta.db')

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

getLatest()
