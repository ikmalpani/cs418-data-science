var results_80_20_split = {
	'class' : [1,2,3,4,5],
	'accuracy' : 0.53,
	'precision' : [0.58,0.42,0.43,0.50,0.64],
	'recall' : [0.54,0.28,0.29,0.69,0.59],
	'f1_score' : [0.56,0.33,0.35,0.58,0.61]
}; // SVM

var results_cv_smote = {
	'class' : [1,2,3,4,5],
	'accuracy' : 0.66,
	'precision' : [0.780133,0.709461,0.620219,0.536074,0.639384],
	'recall' : [0.891520,0.691406,0.575996,0.473240,0.694219],
	'f1_score' : [0.832116,0.700317,0.597290,0.502701,0.665674]
}; // Log Reg


var results_nn_sentiments = {
	'class' : [1,2,3,4,5],
	'accuracy' : 0.48,
	'precision' : [0.563218,0.401961,0.368868,0.492545,0.585115],
	'recall' : [0.376923,0.374088,0.422703,0.546045,0.522261],
	'f1_score' : [0.451613, 0.387524,0.393955,0.517917,0.551904]
}; // LSTM With Sentiments

let myChart3 = document.getElementById('myChart3').getContext('2d');
myChart3.canvas.width = 100;
myChart3.canvas.height = 50;
Chart.defaults.global.defaultFontFamily = 'Lato';
Chart.defaults.global.defaultFontSize = 10;
Chart.defaults.global.defaultFontColor = '#777';

let prediction_comparision = new Chart(myChart3, {
	type:'bar', // bar, horizontalBar, pie, line, doughnut, radar, polarArea
	data:{
		labels:results_80_20_split['class'],
		datasets:[
			{
			label: 'Precision', 
			data:results_80_20_split['precision'],
			backgroundColor: '#da413d', // ['green','blue','pink','red','black','yellow'],
			borderWidth:1,
			borderColor:'#777',
			hoverBorderWidth: 3,
			hoverBorderColor: '#000'
		},
		{
			label: 'Recall', 
			data:results_80_20_split['recall'],
			backgroundColor:'#8ba973', // ['green','blue','pink','red','black','yellow'], //
			borderWidth:1,
			borderColor:'#777',
			hoverBorderWidth: 3,
			hoverBorderColor: '#000'
		},
		{
			label: 'F1 Score', 
			data:results_80_20_split['f1_score'],
			backgroundColor:'#84c9fd', // ['green','blue','pink','red','black','yellow'], //
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
			text:'SVM with 80-20 Train-Test Split',
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
		},
		scales:{
			yAxes:[{
				display: true,
				ticks: {
					beginAtZero: true,
					max:1
				}
			}]
		}
	}
});

////////////////////////////////////////////////////////////////

let myChart4 = document.getElementById('myChart4').getContext('2d');
myChart4.canvas.width = 100;
myChart4.canvas.height = 50;

let prediction_comparision1 = new Chart(myChart4, {
	type:'bar', // bar, horizontalBar, pie, line, doughnut, radar, polarArea
	data:{
		labels:results_cv_smote['class'],
		datasets:[
			{
			label: 'Precision', 
			data:results_cv_smote['precision'],
			backgroundColor: '#da413d', // ['green','blue','pink','red','black','yellow'],
			borderWidth:1,
			borderColor:'#777',
			hoverBorderWidth: 3,
			hoverBorderColor: '#000'
		},
		{
			label: 'Recall', 
			data:results_cv_smote['recall'],
			backgroundColor:'#8ba973', // ['green','blue','pink','red','black','yellow'], //
			borderWidth:1,
			borderColor:'#777',
			hoverBorderWidth: 3,
			hoverBorderColor: '#000'
		},
		{
			label: 'F1 Score', 
			data:results_cv_smote['f1_score'],
			backgroundColor:'#84c9fd', // ['green','blue','pink','red','black','yellow'], //
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
			text:'LogReg with SMOTE and 10 CV',
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
		},
		scales:{
			yAxes:[{
				display: true,
				ticks: {
					beginAtZero: true,
					max:1
				}
			}]
		}
	}
});

let myChart5 = document.getElementById('myChart5').getContext('2d');
myChart5.canvas.width = 100;
myChart5.canvas.height = 50;

let prediction_comparision2 = new Chart(myChart5, {
	type:'bar', // bar, horizontalBar, pie, line, doughnut, radar, polarArea
	data:{
		labels:results_nn_sentiments['class'],
		datasets:[
			{
			label: 'Precision', 
			data:results_nn_sentiments['precision'],
			backgroundColor: '#da413d', // ['green','blue','pink','red','black','yellow'],
			borderWidth:1,
			borderColor:'#777',
			hoverBorderWidth: 3,
			hoverBorderColor: '#000'
		},
		{
			label: 'Recall', 
			data:results_nn_sentiments['recall'],
			backgroundColor:'#8ba973', // ['green','blue','pink','red','black','yellow'], //
			borderWidth:1,
			borderColor:'#777',
			hoverBorderWidth: 3,
			hoverBorderColor: '#000'
		},
		{
			label: 'F1 Score', 
			data:results_nn_sentiments['f1_score'],
			backgroundColor:'#84c9fd', // ['green','blue','pink','red','black','yellow'], //
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
			text:'LSTM with input from Sentiment Analysis',
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
		},
		scales:{
			yAxes:[{
				display: true,
				ticks: {
					beginAtZero: true,
					max:1
				}
			}]
		}
	}
});