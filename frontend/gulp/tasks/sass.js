'use strict';

var gulp = require('gulp');
var sass = require('gulp-sass');
var sourcemaps = require('gulp-sourcemaps');
var filePath = require('./filePath.js');
var rename = require('gulp-rename');
var path = require('path');

module.exports = function () {
  return gulp.src('./src/sass/pages/*.scss')
    .pipe(sourcemaps.init())
      .pipe(sass({outputStyle: 'compressed'}).on('error', sass.logError))
    .pipe(sourcemaps.write())
    .pipe(rename(function(p){
      p.dirname = path.join(filePath(p.basename),'css');
    }))
    .pipe(gulp.dest('/'));
};
