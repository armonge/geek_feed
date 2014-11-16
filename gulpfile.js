/*
 * gulpfile.js
 * Copyright (C) 2014 armonge <armonge@reyes-ramirez-1>
 *
 * Distributed under terms of the MIT license.
 */

var gulp           = require('gulp'),
    concat         = require('gulp-concat'),
    bower          = require('gulp-bower'),
    rimraf         = require('gulp-rimraf'),
    mainBowerFiles = require('main-bower-files'),
    path              = require('path'),
    _              = require('lodash'),
    runSequence    = require('run-sequence'),
    templateCache = require('gulp-angular-templatecache'),
    sourcemaps     = require('gulp-sourcemaps');

var base           = 'app/static/src',
    dest           = 'app/static/dist';


var jsFiles        = applyPrefix(base, ['/js/**/*.js']),
    cssFiles = applyPrefix(base, ['/css/**/*.css']),
    templateFiles        = applyPrefix(base, ['/views/**/*.html']);


gulp.task('default', function(cb) {
    runSequence(
        'clean',
        ['scripts', 'templates', 'styles', 'bower'],
        'run',
        cb
    );

});
gulp.task('templates', function(){
  return gulp.src(templateFiles)
          .pipe(templateCache({
            'module': 'geek_feed',
            'root': '',
            base: function(file){
              return 'templates/' + path.basename(file.relative);
            }
          }))
          .pipe(gulp.dest('./app/static/dist/js'));
});

gulp.task('run', function(){
    gulp.watch(jsFiles, ['scripts']);
    gulp.watch(templateFiles, ['templates']);
    gulp.watch('bower.json', ['bower']);
});

gulp.task('clean', function(){
    return gulp.src(dest).pipe(rimraf());
});

gulp.task('scripts', function(){
    gulp.src(jsFiles)
    .pipe(sourcemaps.init())
    .pipe(concat('scripts.js'))
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest('./app/static/dist/js/'));
});

gulp.task('styles', function(){
    gulp.src(cssFiles)
    .pipe(sourcemaps.init())
    .pipe(concat('styles.css'))
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest('./app/static/dist/css/'));
});

gulp.task('bower', function(cb){
    runSequence(
        'bower:collect',
        ['bower:scripts', 'bower:styles'],
        cb
    );
});

gulp.task('bower:collect', function(){
    return bower()
    .pipe(gulp.dest('./app/static/dist/lib'));
});

gulp.task('bower:scripts', function(){
    return gulp.src(mainBowerFiles({filter: '**/*.js'}))
    .pipe(sourcemaps.init())
    .pipe(concat('lib.js'))
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest('./app/static/dist/js'));
});

gulp.task('bower:styles', function(){
    return gulp.src(mainBowerFiles({filter: '**/*.css'}))
    .pipe(concat('lib.css'))
    .pipe(gulp.dest('./app/static/dist/css'));
});

function applyPrefix(prefix, patterns) {
  return _.map(patterns, function(pattern) {
    if (pattern.indexOf('!') >= 0) {
      return '!' + prefix + pattern.replace('!', '');
    }
    return prefix + pattern;
  });
}
