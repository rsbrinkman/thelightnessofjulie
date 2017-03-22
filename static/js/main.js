var user;
var hue = jsHue();
hue.discover(
    function(bridges) {
        if(bridges.length === 0) {
            console.log('No bridges found. :(');
            alert("Whoops, I can't find the bridge. You should probably have Scott take a look at it. ")
        }
        else {
            bridges.forEach(function(b) {
                console.log('Bridge found at IP address %s.', b.internalipaddress);
                ajax.get('/update_ip', {'ip':b.internalipaddress}, function(data){}); 
           
            });
        }
    },
    function(error) {
        console.error(error.message);
        alert("ERROR!!! NOOOO " + error.message)
    }
);

function setLightState(state, bri=false) {
  var settings = ajax.get('/get_settings', '', function(data){
    var results = JSON.parse(data);
    var bridge = hue.bridge(results.ip);
    var user = bridge.user('aREks51uQO6TPSP-T94zMFYDMA0WCuJDXmBWJM7Q');
 
    var lights = user.getLights(function(data) {
      for (light in data) {
        if (state == 'dinner') {
          user.setLightState(light, {bri: Number(results.dinner), on: true});
        }
        if (state == 'snuggle') {
          user.setLightState(light, {bri: Number(results.snuggle), on: true});
        }
        if (state == 'movie') {
          user.setLightState(light, {bri: Number(results.movie), on: true});
        }
        if (state == 'sleep') {
          user.setLightState(light, {on: false});
        }
        if (state == 'love') {
          user.setLightState(light, {bri: Number(results.love), on: true});
        }
        if (state == 'cook') {
          user.setLightState(light, {bri: Number(results.cook), on: true});
        }
        if (bri) {
          user.setLightState(light, {bri: Number(bri), on: true});
        }
      } 
    });
  });
  
}

var dinner = document.getElementById("dinner");
if (dinner) {
  dinner.addEventListener("click", function() {
    setLightState('dinner'); 
  });
}
var love = document.getElementById("love");
if (love) {
  love.addEventListener("click", function() {
    setLightState('love'); 
  });
}
var snuggle = document.getElementById("snuggle");
if (snuggle) {
  snuggle.addEventListener("click", function() {
    setLightState('snuggle'); 
  });
}
var sleep = document.getElementById("sleep");
if (sleep) {
  sleep.addEventListener("click", function() {
    setLightState('sleep'); 
  });
}
var cook = document.getElementById("cook");
if (cook) {
  cook.addEventListener("click", function() {
    setLightState('cook'); 
  });
}
var movie = document.getElementById("movie");
if (movie) {
  movie.addEventListener("click", function() {
    setLightState('movie'); 
  });
}
document.addEventListener('DOMContentLoaded', function () {
  var light = document.getElementById("light");
  if (light) {
    light.addEventListener("change", function() {
      var value = light.value;
      setLightState('custom', value); 
    });
  }
});
var ajax = {};
ajax.x = function () {
    if (typeof XMLHttpRequest !== 'undefined') {
        return new XMLHttpRequest();
    }
    var versions = [
        "MSXML2.XmlHttp.6.0",
        "MSXML2.XmlHttp.5.0",
        "MSXML2.XmlHttp.4.0",
        "MSXML2.XmlHttp.3.0",
        "MSXML2.XmlHttp.2.0",
        "Microsoft.XmlHttp"
    ];

    var xhr;
    for (var i = 0; i < versions.length; i++) {
        try {
            xhr = new ActiveXObject(versions[i]);
            break;
        } catch (e) {
        }
    }
    return xhr;
};

ajax.send = function (url, callback, method, data, async) {
    if (async === undefined) {
        async = true;
    }
    var x = ajax.x();
    x.open(method, url, async);
    x.onreadystatechange = function () {
        if (x.readyState == 4) {
            callback(x.responseText)
        }
    };
    if (method == 'POST') {
        x.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    }
    x.send(data)
};

ajax.get = function (url, data, callback, async) {
    var query = [];
    for (var key in data) {
        query.push(encodeURIComponent(key) + '=' + encodeURIComponent(data[key]));
    }
    ajax.send(url + (query.length ? '?' + query.join('&') : ''), callback, 'GET', null, async)
};

ajax.post = function (url, data, callback, async) {
    var query = [];
    for (var key in data) {
        query.push(encodeURIComponent(key) + '=' + encodeURIComponent(data[key]));
    }
    ajax.send(url, callback, 'POST', query.join('&'), async)
};

