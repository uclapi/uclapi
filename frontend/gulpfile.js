var gulp = require('./gulp')([
  'browserify',
  'sass',
  'watch'
]);

gulp.task('build', ['browserify', 'sass']);
gulp.task('default', ['build', 'watch']);
