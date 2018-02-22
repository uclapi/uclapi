'use strict';

var browserify = require('browserify');
var gulp = require('gulp');
var gutil = require('gulp-util');
var source = require('vinyl-source-stream');
var buffer = require('vinyl-buffer');
var glob = require('glob');
var path = require('path');
var uglify = require('gulp-uglify');
var sass = require('gulp-sass');
var rename = require('gulp-rename');
var fileModules = require('./fileModules.json');


function getFilePath(fileName) {
    // UCL API Base Directory Path
    var baseDir = path.resolve(__dirname, '../../../');
    var fileModule = fileModules[fileName];
    return path.join(baseDir, "artifact", "frontend", fileModule, fileName + '.js');
}

function removeExtentionAndPath(file, extension){
  var extStart = file.indexOf('.' + extension);
  var fileStart = file.lastIndexOf('/');
  return file.slice(fileStart + 1, extStart);
}

function browserified(filename) {
  var b = browserify(filename);
  var fileNoExt = removeExtentionAndPath(filename, 'jsx');
  var p = getFilePath(fileNoExt);
  b.bundle()
    .on('error', gutil.log)
    .pipe(source(fileNoExt + '.js'))
    .pipe(buffer())
    .pipe(uglify())
    .pipe(gulp.dest(path.join(p, 'js')));
}

module.exports = function() {
  glob('./src/react/pages/*.jsx', {}, function(err, files){
    files.forEach(browserified);
  });
  gulp.src('./src/sass/pages/*.scss')
    .pipe(sass({outputStyle: 'compressed'}).on('error', sass.logError))
    .pipe(rename(function(p){
      p.dirname = path.join(getFilePath(p.basename),'css');
    }))
    .pipe(gulp.dest('/'));
};
