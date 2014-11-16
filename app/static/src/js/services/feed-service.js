angular.module('geek_feed')
.service('Feeds', function ($http, $pusher, PUSHER_KEY) {
    var self = this;
    var feedsD = $http.get('/api/feeds');
    feedsD.then(function(response){
        self.feeds = response.data.feeds;
    });

    var client = new Pusher(PUSHER_KEY);
    var pusher = $pusher(client);
    var feedsChannel = pusher.subscribe('feeds');

    feedsChannel.bind('new-feed', function(data){
        self.feeds.push(angular.fromJson(data));
    });

    self.getEvents = function(feedSlug){
        return $http.get('/api/feeds/' + feedSlug).then(function(response){
            return response.data;
        });
    }

    self.get = function(feedSlug){
        var channel = pusher.subscribe(feedSlug);
        return feedsD.then(function(){
            var feed = _.find(self.feeds, {'slug': feedSlug});
            channel.bind('new-event', function(data){
                feed.events.push(angular.fromJson(data));
            });

            if(!feed.events){
                return self.getEvents(feedSlug);
            }else{
                return feed;
            }
        });
    };

    return self;
});
