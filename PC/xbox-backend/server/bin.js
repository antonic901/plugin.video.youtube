'use-strict'

let process = require('process'),
    network = require('./utils/network');

process.title = 'xbox-backend';

let host = process.env.HOST || network.getHostAddress();
let port = process.env.PORT || 9007;

let http = require('http'),
    api = require('./');

let server = http.createServer(api);

server.listen(port, host).on('error', function (e) {
    if (e.code !== 'EADDRINUSE' && e.code !== 'EACCES') {
        throw e;
    }
    console.log('Port ' + port + ' is busy. Trying the next available port...');
    server.listen(++port);
}).on('listening', function () {
    console.log('API is successfully started. Listening on http://' + host + ':' + port);
});

module.exports = { host, port };