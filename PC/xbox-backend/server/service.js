'use strict';

let axios = require('axios');

function createConfig(type, url, headers, query, body) {
    let config = {
        url: url,
        method: type,
        headers: {accept: 'application/json'},
        params: query
    };
    if (type !== 'get') {
        config.data = body;
    }
    return config;
}

async function makeRequest(type, url, headers, query, body) {
    let config = createConfig(type, url, headers, query, body);
    console.log(config);
    try {
        let response = await axios.get(url, config);
        return {
            success: true,
            status: response.status,
            body: response.data
        }
    } catch (err) {
        try {
            return {
                succcess: false,
                status: err.response.status,
                body: err.response.data
            }
        } catch (err) {
            return {
                success: true,
                status: 404,
                body: 'This API seems to be offline.'
            }
        }
    }
}

module.exports = { makeRequest }