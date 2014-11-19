angular.module('geek_feed')
.factory('socket', function ($rootScope, $window, CHANNEL_TOKEN) {
    var channel = new goog.appengine.Channel(CHANNEL_TOKEN);
    var socket = channel.open();

    var listeners = {};
    socket.onmessage = function(message){
        var data = angular.fromJson(message.data);
        console.log(message, data);

        _.each(listeners[data.event], function(fn){
            $rootScope.$apply(function(){
                fn(data.data);
            });
        });
    };

    socket.onopen = function(){
        console.log('Connected to channel');
    };
    socket.onclose = function(){
        console.log('Closed channel');
    };
    socket.onerror = function(data){
        console.log('Error channel', data);
    };

    return {
        on: function(event, fn){
            if(!listeners[event]){
                listeners[event] = [];
            }

            listeners[event].push(fn);
        }
    };
});
