/*
 * This is used to calculate the absolute file path to build static files into.
 *
 * Potentially in the future we may have more than just the dashboard that requires frontend
 * so instead of hard coding in the path caculate it dynamically from fileModules.json
 *
 */
var path = require('path');
var fileModules = require('./fileModules.json');

var baseDir = path.resolve(__dirname, '../../../'); //gets absolute path to UCLAPI base directory
var backendPath = 'backend/uclapi/';


module.exports = function filePath(fileName){
  var fileModule = fileModules[fileName];
  return path.join(baseDir, backendPath, fileModule, 'static');
};
