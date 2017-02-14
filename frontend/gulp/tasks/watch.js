var gulp = require('gulp');

module.exports = function() {
  gulp.watch('./src/react/**/*.jsx', ['browserify']);
  gulp.watch('./src/sass/**/*.scss', ['sass']);
};
