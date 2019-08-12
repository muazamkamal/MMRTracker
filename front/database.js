var fs = require('fs')
var path = require('path')
var initSqlJs = require('./sql-wasm')
var filebuffer = fs.readFileSync(path.join(__dirname, '../back/s3_1_beta.db'))

function read () {
  initSqlJs().then(SQL => {
    // Create a database
    var db = new SQL.Database(filebuffer)
    // NOTE: You can also use new SQL.Database(data) where
    // data is an Uint8Array representing an SQLite database file

    // Prepare an sql statement
    db.each('SELECT * FROM mmr ORDER BY time DESC LIMIT 1',
      function (row) { console.log(row.time + ': ' + row.core) }
    )
  })
}
