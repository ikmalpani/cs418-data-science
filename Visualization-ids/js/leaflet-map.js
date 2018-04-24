// set the map center and zoom level
var map = L.map( 'map', {
    center: [41.8781, -87.6298],
    minZoom: 2,
    zoom: 14
});

// set the map tile
// L.tileLayer('https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png', {
//     attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="http://cartodb.com/attributions">CartoDB</a>',
//     subdomains: 'abcd'
// }).addTo(map);

L.tileLayer('https://cartodb-basemaps-{s}.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="http://cartodb.com/attributions">CartoDB</a>',
    subdomains: 'abcd',
    maxZoom: 19
}).addTo(map);

// read json and store in "markers"
var markers = $.ajax({
    async: false,
    url: 'json/q1Data.json',
    dataType: 'json'
}).responseJSON;

// console.log(markers.length)

function getColor(btype){
    switch (btype) {
    case 'restaurant':
        return  '#ff6766';
    case 'grocery store':
        return '#79c879';
    case 'school':
        return '#ffb366';
    }
}

// needs to be fixed
function getOpacity(crimes){
    if(crimes >=1 && crimes <=4) return 0.2;
    else if(crimes >=5 && crimes <= 8) return 0.4;
    else if(crimes >= 10 && crimes <= 18) return 0.6;
    else if(crimes >= 19 && crimes <= 200) return 0.8;
    else if(crimes > 200) return 1;
}

// loop through the data and plot on map
for ( var i=0; i < markers.length; ++i )
{
    L.circleMarker( [markers[i].Latitude, markers[i].Longitude], {radius: 6, color: getColor(markers[i]['Business Type']), fillOpacity: getOpacity(markers[i]['#Crimes'])} )
        .bindPopup( '<p>'+
            markers[i]['Business Name'] + '</br>'+
            markers[i]['Business Type'] + '</br>'+
            '<b>Crimes: </b>'+  markers[i]['#Crimes']+ '</br>'+
            '<b>Arrests: </b>'+ markers[i]['#Arrests'] +'</p>')
        .addTo( map );
}


// console.log(test.length);
