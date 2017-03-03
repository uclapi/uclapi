var gulp = require('./gulp')([
  'browserify',
  'sass',
  'watch',
  'productionBuild'
]);

gulp.task('set-prod-node-env', function() {
  return process.env.NODE_ENV = 'production';
});

gulp.task('build', ['browserify', 'sass']);
gulp.task('production', ['set-prod-node-env', 'productionBuild']);
gulp.task('default', ['build', 'watch']);
