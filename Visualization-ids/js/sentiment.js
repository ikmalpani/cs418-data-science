var ratings = {
	'rating': [1,2,3,4,5],
	'count' : [1915,2575,4756,8651,6961],
	'negative_ratings' : [1490,1463,1522,1508,890],
	'positive_ratings' : [425,1112,3234,7143,6071]
	};

let myChart = document.getElementById('myChart').getContext('2d');
myChart.canvas.width = 100;
myChart.canvas.height = 50;
Chart.defaults.global.defaultFontFamily = 'Lato';
Chart.defaults.global.defaultFontSize = 10;
Chart.defaults.global.defaultFontColor = '#777';

let final_comparision_chart = new Chart(myChart, {
	type:'bar', // bar, horizontalBar, pie, line, doughnut, radar, polarArea
	data:{
		labels:ratings['rating'],
		datasets:[
			{
			label: 'Negative Ratings Count', 
			data:ratings['negative_ratings'],
			backgroundColor: 'rgba(255, 0, 0, 0.6)', // ['green','blue','pink','red','black','yellow'],
			borderWidth:1,
			borderColor:'#777',
			hoverBorderWidth: 3,
			hoverBorderColor: '#000'
		},
		{
			label: 'Positive Ratings Count', 
			data:ratings['positive_ratings'],
			backgroundColor:'rgba(0, 255, 0, 0.6)', // ['green','blue','pink','red','black','yellow'], //
			borderWidth:1,
			borderColor:'#777',
			hoverBorderWidth: 3,
			hoverBorderColor: '#000'
		},
		{
			label: 'Actual Rating Count', 
			data:ratings['count'],
			backgroundColor:'rgba(0, 0, 255, 0.6)', // ['green','blue','pink','red','black','yellow'], //
			borderWidth:1,
			borderColor:'#777',
			hoverBorderWidth: 3,
			hoverBorderColor: '#000'
		}
		]
	},
	options:{
		title:{
			display:true,
			text:'Positive/Negative Prediction vs Actual Ratings',
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

var average_sentiments = {
	'type': ['positive', 'negative'],
	'ratings': [1445,584]
};

let myChart1 = document.getElementById('myChart1').getContext('2d');
myChart1.canvas.width = 100;
myChart1.canvas.height = 50;

let predicted_ratings_count = new Chart(myChart1, {
	type:'doughnut', // bar, horizontalBar, pie, line, doughnut, radar, polarArea
	data:{
		labels:average_sentiments['type'],
		datasets:[
			{
			label: '# Ratings', 
			data:average_sentiments['ratings'],
			backgroundColor: ['rgba(0, 255, 0, 0.6)','rgba(255, 0, 0, 0.6)'], // ['green','blue','pink','red','black','yellow'],
			borderWidth:1,
			borderColor:'#777',
			hoverBorderWidth: 3,
			hoverBorderColor: '#000'
		}]
	},
	options:{
		title:{
			display:true,
			text:'Number of Predicted Positive/Negative Ratings',
			fontSize: 25,
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

var all_ratings = {
	'rating': [1,2,3,4,5],
	'count' : [1915,2575,4756,8651,6961]
	};

let myChart2 = document.getElementById('myChart2').getContext('2d');
myChart2.canvas.width = 100;
myChart2.canvas.height = 50;

let ratings_count_chart = new Chart(myChart2, {
	type:'polarArea', // bar, horizontalBar, pie, line, doughnut, radar, polarArea
	data:{
		labels:all_ratings['rating'],
		datasets:[
			{
			label: '# Ratings', 
			data:all_ratings['count'],
			backgroundColor: ['red','orange','yellow','rgb(50,205,50)','green'],
			borderWidth:1,
			borderColor:'#777',
			hoverBorderWidth: 3,
			hoverBorderColor: '#000'
		}]
	},
	options:{
		title:{
			display:true,
			text:'Number of Actual Ratings',
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
