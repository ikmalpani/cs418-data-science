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
var ctx = document.getElementById("q8Chart").getContext("2d");

q8Chart = new Chart(ctx, {
   type: "bar"
});

function drawQ8Chart(q8Data){
    var labels=[], years=[];
    dataByYear.forEach(function(d){
        labels.push(d['RestaurantName']);
        years.push(parseFloat(d['AliveForXyears']));
        console.log(years)

    });

    if(q8Chart){
        q8Chart.destroy();
    }

    q8Chart = new Chart(ctx, {
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




