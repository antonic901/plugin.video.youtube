'use strict';

const os = require('os');

/* >> This function returns IP Address
of Server on which API is running << */
function getHostAddress() {    
    const nets = os.networkInterfaces();
    const results = Object.create(null); // Or just '{}', an empty object
    var host = null;
  
    for (const name of Object.keys(nets)) {
        for (const net of nets[name]) {
            // Skip over non-IPv4 and internal (i.e. 127.0.0.1) addresses
            if (net.family === 'IPv4' && !net.internal) {
                if (!results[name]) {
                    results[name] = [];
                }
                results[name].push(net.address);
                host = net.address;
            }
        }
    }
    return host;
  };

  module.exports = {
      getHostAddress
  }