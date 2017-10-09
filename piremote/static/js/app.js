'use strict'; // mandatory to work with angular
// used to parse the password inserted
function getSetting(name, defaultVal) {
		// local storage is used in JS to store data locally within
		// the user's browser
		var val = localStorage.getItem(name);
		if (val === null) {
      
       return defaultVal;
   }
   try {
      // parsing the password
      return JSON.parse(val);
   } catch (e) {
      if (typeof(console) !== "undefined")
         console.log("Error parsing setting '" + name + "': " + val);
      return defaultVal;
   }
}

// angular module that defines the application
var app = angular.module('piremote', []);
// websocket
var ws = null;

// define root controller
app.controller('RootController', function($scope, $rootScope) {
   $scope.page = "auth";

   $scope.switchPage = function(newPage) {
      $scope.page = newPage;
   }
});

// define login controller
app.controller('LoginController', function($scope, $rootScope) {
   // gets password from localStorage
   $scope.password = getSetting("piremote.password", "");

   $scope.connecting = false;

   $scope.alert = {
      "show": false,
      "class": "warning",
      "message": ""
   };

    $scope.wsOnMessage = function(e) { $scope.$apply(function() {
      var msg = e.data;
      $scope.alert.show = false;
      if (msg == "Access granted") {
         $scope.connecting = false;
         $scope.onSuccess();
      } else if (msg == "Access denied") {
         $scope.connecting = false;
         $scope.alert = {
            'show': true,
            'class': 'warning',
            'message': "Access denied."
         };
      } else {
         $scope.connecting = false;
         $scope.alert = {
            'show': true,
            'class': 'danger',
            'message': "The server is broken."
         };
      }
   }); }

   $scope.wsOnError = function(e) { $scope.$apply(function() {
      $scope.connecting = false;
      $scope.alert = {
         'show': true,
         'class': 'danger',
         'message': "Connection failed. Please retry."
      };
   }); }


   $scope.onSuccess = function() {

      // Unbind onmessage (no messages should be show in this page anymore)
      ws.onmessage = function() {}

      // Switch to control page
      $scope.switchPage("control");
   }

   $scope.connect = function() {
      $scope.connecting = true;
      // open websocket
      ws = new WebSocket('ws://' + location.host + '/control?key=' +
         encodeURIComponent($scope.password));
      ws.onmessage = $scope.wsOnMessage;
      ws.onerror = $scope.wsOnError;
      console.log("connect()");

   }
});

// controller for the second page
app.controller('ControlController', function($scope, $rootScope) {

   $scope.vibrate = function() {
      if ("vibrate" in navigator) {
         navigator.vibrate(5);
}
   };

   // functions to control buttons
    
   $scope.previous = function() {
      ws.send("prev");
   };
   $scope.next = function() {
      ws.send("next");
   };

   $scope.presentationMode = function() {
      ws.send("presentation_mode");
   };

   $scope.open = function() {
      ws.send("open");
   };

   $scope.down = function() {
      ws.send("down");
   };

   $scope.up = function() {
      ws.send("up");
   };

   $scope.enter = function() {
      ws.send("enter");
   };

   $scope.escape = function() {
      ws.send("escape");
   };

   // init alert message
   $scope.alert = {
      "show": false,
      "class": "warning",
      "message": ""
   }

   $scope.disconnected = false;

   $scope.wsOnError = function() { $scope.$apply(function() {
      $scope.alert = {
         "show": true,
         "class": "danger",
         "message": "Connection with server was lost"
      };
      $scope.disconnected = true;
   }); };

   // used for reconnection in case connection with server is lost
   $scope.reconnect = function() {
      $scope.switchPage("auth");
   }

   ws.onerror = $scope.wsOnError;
   ws.onclose = $scope.wsOnError;
});