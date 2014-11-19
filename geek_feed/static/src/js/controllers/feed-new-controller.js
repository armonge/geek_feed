angular.module('geek_feed')
.controller('FeedCreateCtrl', function ($scope, Feeds) {
    $scope.createFeed = function(match){
        if($scope.form.$valid){
            Feeds.createMatch(match);
        }
    };
});
