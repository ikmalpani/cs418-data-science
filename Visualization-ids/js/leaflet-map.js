// set the map center and zoom level
var map = L.map( 'map', {
    center: [41.87451215, -87.63986471],
    minZoom: 2,
    zoom: 14
});

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
    if(crimes >=1 && crimes <=5) return 0.3;
    else if(crimes >=6 && crimes <= 30) return 0.5;
    else if(crimes > 30 && crimes <= 100) return 0.7;
    else if(crimes > 100 && crimes <= 300) return 0.9;
    else if(crimes > 300) return 1;
}

var lat,lng;
function getLatitudeLongitude(){
    lat = this.getLatLng().lat;
    lng = this.getLatLng().lng;
    // console.log(lat, lng);
    drawQ1Chart();
}

// loop through the data and plot on map
for ( var i=0; i < markers.length; ++i )
{
    L.circleMarker( [markers[i].Latitude, markers[i].Longitude], {radius: 6, color: getColor(markers[i]['Business Type']), fillOpacity: getOpacity(markers[i]['#Crimes'])} )
        .bindPopup( '<p>'+
            markers[i]['Business Name'] + '</br>'+
            markers[i]['Business Type'] + '</br>'+
            '<b>Crimes: </b>'+  markers[i]['#Crimes']+ '</br>'+
            '<b>Arrests: </b>'+ markers[i]['#Arrests'] + '</br>'+
            '<b>Has Tobacco License: </b>' + markers[i]['Has Tobacco License']+'</br>'+
            '<b>Has Liquor License: </b>'+ markers[i]['Has Liquor License']+'</p>')
        .addTo( map ).on('click',getLatitudeLongitude);
}


var q1Data = $.ajax({
   async: false,
   url: 'json/Query1_Results.json',
   dataType: 'json'
}).responseJSON;

defaultData = q1Data.filter(q => q.Latitude == 41.88802499);
// console.log(defaultData);

var defaultlabels2 = [], defaultData2 = [], defaultTitle = '', defaultBType = '';
defaultData.forEach(function(d){
  defaultlabels2.push(d['Crime Type']);
  defaultData2.push(d['#Crimes']);
  defaultTitle = d['Business Name'];
  defaultBType = d['Business Type'];
});


var newChart;
var ctx = document.getElementById("q1Chart").getContext("2d");

newChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: defaultlabels2,
      datasets: [{
          label: 'Crime distribution within 3 blocks of ' + defaultTitle,
          backgroundColor: getColor(defaultBType),
          data: defaultData2
      }]
    }
});

function drawQ1Chart(){
    var labels = [], data = [];
    var title, btype = '', barColor = '';
    q1Data.forEach(function(d){
        if(d['Latitude'] == lat && d['Longitude'] == lng){
        labels.push(d['Crime Type']);
        data.push(d['#Crimes']);
        title = d['Business Name'];
        btype = d['Business Type'];
        }
    });

    var Data = {
        labels: labels,
        datasets: [{
            label: 'Crime distribution within 3 blocks of ' + title,
            backgroundColor: getColor(btype),
            data: data
        }]
    };

    if(newChart){
        newChart.destroy();
    }

    // Instantiate a new chart
    newChart = new Chart(ctx , {
        type: "bar",
        data: Data,
        options: {
            scales: {
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'Number of Crimes'
                    },
                    ticks: {
                        beginAtZero: true,
                        stepSize: 50
                        // max: 600
                    }
                }],
                xAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'Crime Types'
                    }
                }]
            }
        }
    });
}
