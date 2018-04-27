var q8 = $.ajax({
    async: false,
    url: 'json/Query8_Results.json',
    dataType: 'json'
}).responseJSON;



var dataByYear = [];

// var charts = [];
$("#Year").on("change", function () {

    var selectedVal = $(this).find(':selected').val();
    // console.log(selectedVal);
    dataByYear = q8.filter(q => q.YearOfInspection == selectedVal)
    // console.log(dataByYear[1]['Failedinspectionon'])

    drawQ8Chart(dataByYear);
});

var q8Chart;
var ctx8 = document.getElementById("q8Chart").getContext("2d");

var data2010 = [];
data2010 = q8.filter(q => q.YearOfInspection == 2010);
console.log(data2010);

var labels2010=[], years2010=[];
data2010.forEach(function(d){
    labels2010.push(d['RestaurantName']);
    years2010.push(parseFloat(d['AliveForXyears']));
    // console.log(years)

});

q8Chart = new Chart(ctx8, {
   type: "bar",
    data: {
        labels : labels2010,
        datasets : [{
            label: "Viability of Business",
            backgroundColor: '#ff6766',
            data: years2010}],
    },
    options: {
        scales: {
            yAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: 'Years'
                }
            }],
            xAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: 'Restaurant Name'
                }
            }]
        }
    }
});

function drawQ8Chart(q8Data){
    var labels=[], years=[];
    dataByYear.forEach(function(d){
        labels.push(d['RestaurantName']);
        years.push(parseFloat(d['AliveForXyears']));
        // console.log(years)

    });

    if(q8Chart){
        q8Chart.destroy();
    }

    q8Chart = new Chart(ctx8, {
       type: 'bar',
       data: {
           labels : labels,
           datasets : [{
               label: "Viability of Business",
               backgroundColor: '#ff6766',
                data: years}],
       },
        options: {
            scales: {
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'Years'
                    }
                }],
                xAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'Restaurant Name'
                    }
                }]
            }
        }

    });

}




