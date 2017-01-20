var browserify = require('browserify');
var gulp = require('gulp');
var uglify = require('gulp-uglify');
var source = require('vinyl-source-stream');
var buffer = require('vinyl-buffer');
var gutil = require('gulp-util');
var less = require('gulp-less');
var cleanCSS = require('gulp-clean-css');
//var stripDebug = require('gulp-strip-debug');

module.exports = function(){
  var b = browserify({
    entries: './views/app.jsx',
    debug: true
  });
  b.bundle()
    .pipe(source('app.js'))
    .pipe(buffer())
//    .pipe(stripDebug())
    .pipe(uglify())
    .on('error', gutil.log)
    .pipe(gulp.dest('./production/js/'));
  gulp.src('./views/index.less')
    .pipe(less())
    .pipe(cleanCSS())
    .pipe(gulp.dest('./production/css/'));
};
