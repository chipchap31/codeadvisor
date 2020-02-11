"use strict";
var dialog = (function(){


  function open(id){

    var target = document.getElementById(`dialog_${id}`);
    target.classList.add('open')
  }
  function close(id){
    var target = document.getElementById(`dialog_${id}`);
    target.classList.remove('open')
  }
  return { open, close }

})()


// @method pie renders the data information for the languages used
var doughnut = (function(){



    // @ method init draws the chart
    function init (data){
        
        var ctx = document.getElementById(data.name).getContext('2d');
        var chart = new Chart(ctx, {
        // The type of chart we want to create
        type: 'pie',

        // The data for our dataset
        data: {
            labels: data.stack_labels,
            datasets: [{
                
                backgroundColor: [
						'rgb(100, 165, 233)',
						'rgb(253, 217, 141)',
				        'rgb(8, 192, 163)',
					],
				borderColor: [
						'rgb(100, 165, 233)',
						'rgb(253, 217, 141)',
				        'rgb(8, 192, 163)',
					],
              
                data: data.stack_value
            }]
        },

        // Configuration options go here
        options: {
            tooltips: {
              callbacks: {
                label: function(o, i) {
                  return i['labels'][o['index']] + ': ' + i['datasets'][0]['data'][o['index']] + '%';
                }
              }
            }
        }
    });

    }
return { init }
})()




var server = (function(){
    function post(data) {
      return fetch(data.path, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Origin": "*"
        },
        body: JSON.stringify(body)
      })
        .then(function (res){
            return res.json();
        })
        .then(function (res){
            return res
        });
    }
    return { post }
})()
