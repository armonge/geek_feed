angular.module('geek_feed')
.service('Feeds', function ($http, socket) {
    var self = this;
    var feedsD = $http.get('/api/feeds');

    feedsD.then(function(response){
        self.feeds = response.data.feeds;
    });

    socket.on('new-feed', function newFeed(data){
        self.feeds.push(data);
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

            if(!self.feeds[feedIndex].events){
                socket.on('new-event:'+feedSlug, function(data){
                    return self.feeds[feedIndex].events.push(data);
                });
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
