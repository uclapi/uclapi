var gulp = require('./gulp')([
  'browserify',
  'sass',
  'watch',
  'productionBuild',
  'artifactBuild'
]);

gulp.task('set-prod-node-env', function() {
  return process.env.NODE_ENV = 'production';
});

gulp.task('build', ['browserify', 'sass']);
gulp.task('production', ['set-prod-node-env', 'productionBuild']);

gulp.task('artifact', ['set-prod-node-env', 'artifactBuild']);

gulp.task('default', ['build', 'watch']);
