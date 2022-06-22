'use strict';
const fs = require('fs');

function exists(path, file_name) {
    if(fs.existsSync(path + file_name)) {
        return true;
    } else {
        return false;
    }
}

function rename(path, file_name, new_file_name) {
    if (!fs.existsSync(path + file_name)) {
        console.log("Path: '" + path + "' is not valid.");
        return null;
    }
    fs.renameSync(path + file_name, path + new_file_name);
}

function read(path, file_name) {
    if (!fs.existsSync(path + file_name)) {
        return null;
    }
    return fs.readFileSync(path + file_name);
}

function write(path, file_name, data) {
    if (!fs.existsSync(path)) {
        console.log("Path: '" + path + "' is not valid.");
        return null;
    }
    fs.writeFileSync(path + file_name, data);
    return data;
}

function append(path, file_name, data) {
    if (!fs.existsSync(path)) {
        console.log("Path: '" + path + "' is not valid.");
        return null;
    }
    fs.appendFileSync(path + file_name, data);
    return data;
}

module.exports = {
    exists,
    rename,
    read,
    write,
    append
};