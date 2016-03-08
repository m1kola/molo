import gulp from 'gulp';
import defaults from 'lodash/defaults';
import plumber from 'gulp-plumber';
import webpack from 'webpack-stream';
import jscs from 'gulp-jscs';
import jshint from 'gulp-jshint';
import { JSXHINT as linter } from 'jshint-jsx';

import webpackPrd from './conf/webpack.prd.config';
import webpackDev from './conf/webpack.dev.config';


const env = process.env.NODE_ENV || 'dev';


const webpackConf = {
  'dev': webpackDev,
  'prd': webpackPrd
}[env];


const paths = {
  js: [
    '*.js',
    'src/**/*.js'
  ]
};


gulp.task('build:scripts', () => {
  return webpack(webpackConf)
    .pipe(gulp.dest('./dist'));
});


gulp.task('watch:scripts', () => {
  return webpack(defaults(webpackConf, {
    watch: true,
    keepalive: true
  }));
});


gulp.task('lint', () => {
  return gulp.src(paths.js)
    .pipe(plumber())
    .pipe(jscs())
    .pipe(jshint({linter: linter}))
    .pipe(jshint.reporter('jshint-stylish'));
});


gulp.task('watch:lint', () => {
  gulp.watch(paths.js, ['lint']);
});


gulp.task('test', []);
gulp.task('watch', ['watch:lint', 'watch:scripts']);
gulp.task('build', ['build:scripts']);
gulp.task('ci', ['lint', 'build', 'test']);
gulp.task('default', ['build', 'test']);