"use strict";

// @method pie renders the data information for the languages used
var doughnut = (function () {
	// @ method init draws the chart
	function init(data) {

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
						label: function (o, i) {
							return i['labels'][o['index']] + ': ' + i['datasets'][0]['data'][o['index']] + '%';
						}
					}
				}
			}
		});

	}
	return {
		init
	}
})()




var server = (function () {
	function post(data) {
		return fetch(data.path, {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
					"Access-Control-Origin": "*"
				},
				body: JSON.stringify(body)
			})
			.then(function (res) {
				return res.json();
			})
			.then(function (res) {
				return res
			});
	}

	return {
		post
	}
})()

var toggleOpen = (function () {

	function init() {

		// get all buttons with role 'toggleOpen'
		var targets = document.querySelectorAll("[role='toggleOpen']");


		Array.from(targets).forEach(function (element) {
			// for each target add event listener


			element.addEventListener('click', onClickElement)
		})


		function onClickElement(event) {
			// get the element to add the open or close 
			// target to toggle
			// get attribute
			var elementToToggle = document.getElementById(event.target.getAttribute("data-target"))
			if (elementToToggle.classList.contains('open')) {
				elementToToggle.classList.remove('open')
			} else {
				elementToToggle.classList.add('open')
			}
		}

	}

	return {
		init
	}
})()

function onFeedbackPost() {

}


document.addEventListener('DOMContentLoaded', function () {
	// call the functions
	toggleOpen.init()

})