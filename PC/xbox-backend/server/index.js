'use strict';

const INVIDIOUS = "http://tube.cthd.icu";

const { response } = require('express');
let express = require('express'),
    bodyParser = require('body-parser'),
    morgan = require('morgan'),
    service = require('./service');
    
let api = express();

api.use(bodyParser.json());
api.use(morgan('dev'));
api.use(function (req, res, next) {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Methods', 'OPTIONS, POST, GET, PUT, DELETE');
    res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
    next();
});
api.use(express.static('public'));

api.get('/api/v1/stats', function (req, res) {
    res.statusCode = 404;
    res.send('Not implemented!');
});

api.get('/api/v1/videos/:id', function (req, res) {
    service.makeRequest('get', encodeURI(INVIDIOUS + '/api/v1/videos/' + req.params.id), req.headers, req.query, null)
        .then(result => {
            res.statusCode = result.status;
            res.send(result.body);
        })
});

api.get('/api/v1/annotations/:id', function (req, res) {
    res.statusCode = 404;
    res.send('Not implemented!');
});

api.get('/api/v1/comments/:id', function (req, res) {
    res.statusCode = 404;
    res.send('Not implemented!');
});

api.get('/api/v1/captions/:id', function (req, res) {
    res.statusCode = 404;
    res.send('Not implemented!');
});

api.get('/api/v1/trending', function (req, res) {
    service.makeRequest('get', encodeURI(INVIDIOUS + '/api/v1/trending'), req.headers, req.query, null)
        .then(result => {
            res.statusCode = result.status;
            res.send(result.body);
        })
});

api.get('/api/v1/popular', function (req, res) {
    service.makeRequest('get', encodeURI(INVIDIOUS + '/api/v1/popular'), req.headers, req.query, null)
        .then(result => {
            res.statusCode = result.status;
            res.send(result.body);
        })
});

api.get('/api/v1/channels/:ucid', function (req, res) {
    res.statusCode = 404;
    res.send('Not implemented!');
});

api.get('/api/v1/channels/:ucid/videos', function (req, res) {
    res.statusCode = 404;
    res.send('Not implemented!');
});

api.get('/api/v1/channels/:ucid/latest', function (req, res) {
    res.statusCode = 404;
    res.send('Not implemented!');
});

api.get('/api/v1/channels/:ucid/playlists', function (req, res) {
    res.statusCode = 404;
    res.send('Not implemented!');
});

api.get('/api/v1/channels/:ucid/comments', function (req, res) {
    res.statusCode = 404;
    res.send('Not implemented!');
});

api.get('/api/v1/channels/search/:ucid', function (req, res) {
    res.statusCode = 404;
    res.send('Not implemented!');
});

api.get('/api/v1/search/suggestions', function (req, res) {
    res.statusCode = 404;
    res.send('Not implemented!');
});

api.get('/api/v1/search', function (req, res) {
    service.makeRequest('get', encodeURI(INVIDIOUS + '/api/v1/search'), req.headers, req.query, null)
        .then(result => {
            res.statusCode = result.status;
            res.send(result.body);
        })
});

api.get('/api/v1/playlists/:plid', function (req, res) {
    res.statusCode = 404;
    res.send('Not implemented!');
});

api.get('/api/v1/mixes/:rdid', function (req, res) {
    res.statusCode = 404;
    res.send('Not implemented!');
});

module.exports = api;