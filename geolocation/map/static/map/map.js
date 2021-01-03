(function() {
    var markers = {};
    var UPDATE_INTERVAL = 2000;
    var REMAIN_INTERVAL = 10000;
    var mapbox_style = "mapbox://styles/luispedraza/ckjev2tg1mlvu19rpwnyvlzln";
    var mapbox_access_token = "pk.eyJ1IjoibHVpc3BlZHJhemEiLCJhIjoiY2tqZXV2ZDRiOGozajJ5bGIydzlvb2ptayJ9.OT7YCyVo3-yGl4vApJ0c4w";
    // Leaflet init:
    var map = L.map('content-wrapper').setView([0, 0], 3);
    
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', 
    {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'luispedraza/ckjev2tg1mlvu19rpwnyvlzln',
        tileSize: 512,
        zoomOffset: -1,
        accessToken: mapbox_access_token
    }).addTo(map);
    
    
    
    function onMarkerClick(e) {
        var data = e.target.__data;
        e.target.bindPopup("<div>" + data.user_name + ": " + data.msg + "</div>")
        .openPopup();
    };
    
    function onMarkerMouseover(e) {
        e.target.__keep = true;
    };
    
    function onMarkerMouseout(e) {
        e.target.__keep = false;
    };
    
    function update() {
        $.getJSON("/api/twitter", function(data) {
            var newData = [];
            data = JSON.parse(data);
            console.log(data);
            
            data.forEach(function(d, i) {
                if (markers[d.id]) return;
                newData.push(d);
            })
            var itemDelay = UPDATE_INTERVAL/newData.length;
            
            newData.forEach(function(d, i) {
                var marker = L.marker([d.place.lat, d.place.lon], {riseOnHover: true})
                .on("click", onMarkerClick)
                .on("mouseover", onMarkerMouseover)
                .on("mouseout", onMarkerMouseout);
                
                markers[d.id] = marker;
                marker.__data = d;
                marker.__keep = false;
                // Add marker with timeout;
                setTimeout(function() {
                    map.addLayer(marker);	
                }, itemDelay*i);
                // Remove marker with timeout:
                setTimeout(function() {
                    var marker = markers[d.id];
                    if (marker.__keep) {
                        
                    } else {
                        map.removeLayer(marker);	
                    }
                    
                }, REMAIN_INTERVAL + itemDelay*i);
            })
        })	
    }
    
    setInterval(update, UPDATE_INTERVAL);
})();