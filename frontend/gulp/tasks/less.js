var gulp = require('gulp'); 
var less = require('gulp-less');

module.exports =  function() {
  gulp.src('./views/index.less')
    .pipe(less())
    .pipe(gulp.dest('./statics/css/'));
};
