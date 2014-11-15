'use strict';

angular.module('georgeApp')
    .controller('MainCtrl', function ($scope, $http) {
        $scope.msg = "";
        $scope.messages = [{
            author: "George",
            body: "Yo! Type something and I'll answer with a meme!"
        }];

        $scope.msgEntered = function () {
            $scope.messages.push({
                author: "Me",
                body: $scope.msg
            });
            $http.get('http://localhost:5000/api/' + $scope.msg).
                success(function (data, status, headers, config) {
                    $scope.msg = "";
                    $scope.messages.push(data);
                }).
                error(function (data, status, headers, config) {
                    alert(status + " " + data);
                });
        };
    });
