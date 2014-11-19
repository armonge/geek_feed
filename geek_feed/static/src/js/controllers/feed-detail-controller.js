angular.module('geek_feed')
.controller('FeedDetailCtrl', function ($scope, $routeParams, $location, Feeds) {
    Feeds.get($routeParams.slug).then(function(feed){
        if(!feed){
          $location.path('/');
        }

        $scope.feed = feed;
    });
});
