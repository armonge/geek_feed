// Declare app level module which depends on filters, and services
angular.module('geek_feed', [
    'ngResource',
    'ngRoute',
    'ui.bootstrap',
    'ui.date',
    'pusher-angular'])
.config(function ($routeProvider) {
    $routeProvider
    .when('/', {
        templateUrl: 'templates/feed_list.html',
        controller: 'FeedListCtrl'})
    .when('/feed/new-feed', {
        templateUrl: 'templates/feed_new.html',
        controller: 'FeedCreateCtrl'})
    .when('/feed/:slug', {
        templateUrl: 'templates/feed_detail.html',
        controller: 'FeedDetailCtrl'
    }).when('/feed/:slug/push/', {
        templateUrl: 'templates/feed_push.html',
        controller: 'FeedPushCtrl'
    })
    .otherwise({redirectTo: '/'});
});

