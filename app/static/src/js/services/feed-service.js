angular.module('geek_feed')
.service('Feeds', function ($http, $pusher, PUSHER_KEY) {
    var self = this;
    var feedsD = $http.get('/api/feeds');

    self.channels = {};
    self.getChannel = function(channel, feed){
        if(!self.channels[channel]){
            self.channels[channel] = pusher.subscribe(channel);
            self.channels[channel].bind('new-event', function(data){
                feed.events.push(angular.fromJson(data));
            });
        }
        return self.channels[channel];
    };

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
        return $http.get('/api/feeds/' + feedSlug + '/events').then(function(response){
            return response.data.events;
        });
    };

    self.get = function(feedSlug){
        return feedsD.then(function(){
            var feedIndex = _.findIndex(self.feeds, {'slug': feedSlug});
            if(feedIndex === -1){
                return null;
            }

            self.getChannel(feedSlug, self.feeds[feedIndex]);

            if(!self.feeds[feedIndex].events){
                return self.getEvents(feedSlug).then(function(events){
                    self.feeds[feedIndex].events = events;
                    return self.feeds[feedIndex];
                });
            }else{
                return self.feeds[feedIndex];
            }
        });
    };

    self.pushEvent = function(feedSlug, event){
        return $http.post('/api/feeds/'+ feedSlug + '/events', event);
    };

    self.createMatch = function(match){
        return $http.post('/api/feeds', match);
    };

    return self;
});
