var gulp = require('./gulp')([
  'browserify',
  'sass',
  'watch',
  'productionBuild'
]);

gulp.task('build', ['browserify', 'sass']);
gulp.task('default', ['build', 'watch']);
gulp.task('production', ['productionBuild']);
