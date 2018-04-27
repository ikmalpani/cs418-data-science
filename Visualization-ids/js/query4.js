var result = {
    'pass' : [3,7,50,137,80],
    'fail' : [0,0,1,6,1],
    'conditional' : [0,0,2,4,2]
};




var ctx4 = document.getElementById("q4Chart").getContext("2d");

final_chart = new Chart(ctx4, {
    type: 'bar', // bar, horizontalBar, pie, line, doughnut, radar, polarArea
    data: {
        labels: ['0-1','1-2','2-3', '3-4', '4-5'],
        datasets: [
            {
                label: 'Pass',
                data: result["pass"],
                backgroundColor: 'rgba(255, 0, 0, 0.6)', // ['green','blue','pink','red','black','yellow'],
                borderWidth: 1,
                borderColor: '#777',
                hoverBorderWidth: 3,
                hoverBorderColor: '#000'
            },
            {
                label: 'Fail',
                data: result['fail'],
                backgroundColor: 'rgba(0, 255, 0, 0.6)', // ['green','blue','pink','red','black','yellow'], //
                borderWidth: 1,
                borderColor: '#777',
                hoverBorderWidth: 3,
                hoverBorderColor: '#000'
            },
            {
                label: 'Conditional',
                data: result['conditional'],
                backgroundColor: 'rgba(0, 0, 255, 0.6)', // ['green','blue','pink','red','black','yellow'], //
                borderWidth: 1,
                borderColor: '#777',
                hoverBorderWidth: 3,
                hoverBorderColor: '#000'
            }
        ]
    },

    options:{
        title:{
            display:true,
            text:'Relationship Between Rating and Food Inspection Result',
            fontSize: 20,
        },
        legend:{
            display:true,
            position:'right',
            labels:{
                fontColor: 'black'
            }
        },
        layout:{
            padding:{
                left:50,
                right:0,
                bottom:0,
                top:0
            }
        },
        tooltips:{
            enabled:true
        }
    }
});