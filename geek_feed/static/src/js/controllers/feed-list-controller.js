angular.module('geek_feed')
.controller('FeedListCtrl', function ($scope, Feeds) {
    $scope.Feeds = Feeds;
});
