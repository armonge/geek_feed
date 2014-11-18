angular.module('geek_feed')
.factory('socket', function ($rootScope, $window) {
    var socket = new WebSocket('ws://' + $window.location.hostname + '/ws/');
    var listeners = {};
    socket.onmessage = function(message){
        var data = angular.fromJson(message.data);
        var event = data.event;

        _.each(listeners[data.event], function(fn){
            $rootScope.$apply(function(){
                fn(data.data);
            });
        });
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
