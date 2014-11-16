// Declare app level module which depends on filters, and services
angular.module('geek_feed', [
    'ngResource',
    'ngRoute',
    'ui.bootstrap',
    'ui.date',
    'pusher-angular'])
.config(['$routeProvider', function ($routeProvider) {
    $routeProvider
    .when('/', {
        templateUrl: 'templates/feed_list.html',
        controller: 'FeedListCtrl'})
    .when('/feed/:slug', {
        templateUrl: 'templates/feed_detail.html',
        controller: 'FeedDetailCtrl'
    })
    .otherwise({redirectTo: '/'});
}]);
