var map = L.map( 'mapTwo', {
    center: [41.87451215, -87.63986471],
    minZoom: 2,
    zoom: 13
});

L.tileLayer('https://cartodb-basemaps-{s}.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="http://cartodb.com/attributions">CartoDB</a>',
    subdomains: 'abcd',
    maxZoom: 19
}).addTo(map);

var liquorCrimes = $.ajax({
    async: false,
    url: 'json/bizCrimes.json',
    dataType: 'json'
}).responseJSON;

var ageGroupData = $.ajax({
    async: false,
    url: 'json/q3Data.json',
    dataType: 'json'
}).responseJSON;

function getBlockColor(censusTract){
    var color = '';
    liquorCrimes.forEach(function(l){
        if(censusTract == l['Tract']){
            if(l['#Crimes'] >= 1 && l['#Crimes'] < 1000) color = '#fee5d9';
            else if (l['#Crimes'] >= 1000 && l['#Crimes'] < 3000) color = '#fcbba1';
            else if (l['#Crimes'] >= 3000 && l['#Crimes'] < 6000) color = '#fc9272';
            else if (l['#Crimes'] >= 6000 && l['#Crimes'] < 9000) color = '#fb6a4a';
            else if (l['#Crimes'] >= 9000 && l['#Crimes'] < 30000) color = '#de2d26';
            else if (l['#Crimes'] >= 30000 && l['#Crimes'] < 60000) color = '#a50f15';
        }
    });

    return color;
}

function getLiqBiz(tract){
    var number = 0;
    liquorCrimes.forEach(function(l){
       if(tract == l['Tract']){
           number = l['#BusinessWithLiquorLicense'];
       }
    });
    return number
}

function getTractInfo(tract){
    var numberOfBiz = 0, numberOfCrimes = 0, numberOfArrests = 0;
    liquorCrimes.forEach(function(l){
        if(tract == l['Tract']){
            numberOfBiz = l['#BusinessWithLiquorLicense'];
            numberOfCrimes = l['#Crimes'];
            numberOfArrests = l['#Arrests'];
        }
    });

    return [numberOfBiz, numberOfCrimes, numberOfArrests];
}

function getAgeGroupInfo(tract){
    var prevalentAgeGroup = '';
    ageGroupData.forEach(function(t){
       if(tract == t['Census Tract']){
           prevalentAgeGroup = t['AgeGroup'];
       }
    });
    return prevalentAgeGroup;
}

var q10Data = $.ajax({
    async: false,
    url: 'json/dict.json',
    dataType: 'json'
}).responseJSON;

defaultData3 = q10Data.filter(q => q['Census Tract'] == 839100);
console.log(defaultData3);

var defaultlabels3 = ['May','June','July','August'], defaultData3 = [73.02158100000001, 75.0039949999999, 73.40982199999999,  68.2718180000000],
defaultRobberyType =  ['ARMED: HANDGUN','STRONGARM - NO WEAPON', 'AGGRAVATED','STRONGARM - NO WEAPON'];
// defaultData3.forEach(function(d){
//   defaultlabels3.push(d['month']);
//   defaultData3.push(d['Avg Temp']);
//   defaultRobberyType = d['Robbery Type'];
// });


var query10Chart;
var ctx2 = document.getElementById("q10Chart").getContext("2d");

query10Chart = new Chart(ctx2, {
    type: "bar",
    data: {
      labels: defaultlabels3,
      datasets: [{
          label: 'Probability of Robbery Types for Summer 2018 | Census Tract 839100',
          backgroundColor: getBlockColor(839100),
          data: defaultData3
      }]
    },
    options: {
      tooltips: {
          callbacks: {
              label: function(tooltipItem) {
                  return  (tooltipItem.yLabel).toFixed(2) + "  |  " + defaultRobberyType[tooltipItem.index];
              }
          }
      }
    }
});

function q10Chart(){
    var tract = this.feature.properties.tractce10;
    // console.log(tract);
    var labels = [], data = [], robberyType = [];
    q10Data.forEach(function(d){
       if(tract == d['Census Tract']){
           labels.push(d['month']);
           data.push(d['Avg Temp']);
           robberyType.push(d['Robbery Type']);
       }
    });

    var Data = {
        labels: labels,
        datasets: [{
            label: 'Probability of Robbery Types for Summer 2018',
            backgroundColor: getBlockColor(tract),
            data: data
        }]
    };


    if(query10Chart){
        query10Chart.destroy();
    }

    query10Chart = new Chart(ctx2 , {
        type: "bar",
        data: Data,
        options: {
            tooltips: {
                callbacks: {
                    label: function(tooltipItem) {
                        return  (tooltipItem.yLabel).toFixed(2) + "  |  " + robberyType[tooltipItem.index];
                    }
                }
            },
            scales: {
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'Average Temperature'
                    },
                    ticks: {
                        beginAtZero: true,
                        stepSize: 50
                    }
                }],
                xAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'Month'
                    }
                }]
            }
        }
    });


}

$.getJSON('json/censusTracts.geojson',function(tracts){
    L.geoJson(tracts,{
        style: function(feature){
            var fillColor, censusTract = feature.properties.tractce10;
            fillColor = getBlockColor(censusTract);
            return { color: "#999", weight: 1, fillColor: fillColor, fillOpacity: .6 };
        },
        onEachFeature: function(feature, layer){
            var info = getTractInfo(feature.properties.tractce10);
            var prevalentAgeGroup = getAgeGroupInfo(feature.properties.tractce10);
            layer.bindPopup("<strong>"+ "Census Tract: " +feature.properties.tractce10 + "</strong><br>" + "No. of Businesses with Liquor License: " + getLiqBiz(feature.properties.tractce10) +
                            "<br>"+ "Crimes: " + info[1] + "<br>"+ "Arrests: " + info[2] + "<br>" + "Prevalent Age Group: " + prevalentAgeGroup);
            layer.on({click: q10Chart});
        }
    }).addTo(map);
});
