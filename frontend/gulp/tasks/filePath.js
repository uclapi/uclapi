var path = require('path');
var fileModules = require('./fileModules.json');

var baseDir = path.resolve(__dirname, '../../../'); //gets absolute path to UCLAPI base directory
var backendPath = 'backend/uclapi/';

module.exports = function filePath(fileName){
  var fileModule = fileModules[fileName];
  return path.join(baseDir, backendPath, fileModule, 'static');
};
