angular.module('geek_feed')
.controller('FeedPushCtrl', function ($scope, $routeParams, $http, Feeds) {
    Feeds.get($routeParams.slug).then(function(feed){
        $scope.feed = feed;
    });

    $scope.pushEvent = function(event){
        if($scope.form.$valid){
            Feeds.pushEvent($routeParams.slug, $scope.event);
        }
    };
});
