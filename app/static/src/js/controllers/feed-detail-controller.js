angular.module('geek_feed')
.controller('FeedDetailCtrl', function ($scope, $routeParams, Feeds) {
    Feeds.get($routeParams.slug).then(function(feed){
        $scope.feed = feed;
    });
});
