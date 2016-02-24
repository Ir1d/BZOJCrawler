var express = require('express');
var path = require('path');
var app = express();

app.configure(function() {
    app.use(express.static(path.resolve('include')));
    app.use(express.bodyParser());
    app.use(express.logger("short"));
});
app.use(express.static(path.resolve('../html')));
app.get('/', function (req, res) {
  if (req.query.id) {
    console.log('got query on ' + req.query.id);
    res.sendfile(path.resolve(req.query.id + '.html'));
  } else {
    res.send('use things like ?id=1001 to get result');
  }
});

app.listen(process.env.PORT, function () {
  console.log('Example app listening on port!');
});
