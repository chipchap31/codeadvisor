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
		// the server.post() creates a request to the server via POST
		return fetch(data.path, {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
					"Access-Control-Origin": "*"
				},
				body: JSON.stringify(data.body | null)
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
		var targets = document.querySelectorAll("[role='button']");


		Array.from(targets).forEach(function (element) {
			// for each target add event listener
			element.addEventListener('click', onClickElement)
		})


		function onClickElement(event) {
			// get the element to add the open or close 
			// target to toggle
			// get attribute
			var targetArray = event.target.getAttribute("data-target").split(',');

			for (let target of targetArray) {
				target = document.getElementById(target)
				var isOpen = target.classList.contains('open')

				isOpen ? target.classList.remove('open') : target.classList.add('open')

			}
		}

	}

	return {
		init
	}
})()

var toggleLike = (function () {
	function init() {
		var targets = document.querySelectorAll("[role='toggleLike']");
		Array.from(targets).forEach(function (element) {
			// for each target add event listener
			element.addEventListener('click', onClickElement)
		})



		function onClickElement(event) {

			// when user clicks on like or dislike
			// the block of code below runs


			// get the data-target
			var target = event.target.getAttribute("data-target");
			target = document.getElementById(target);
			var targetId = target.getAttribute('id');
			var targetIsOpen = target.classList.contains('open');

			// target amount of like or dislike 
			var targetAmount = document.getElementById(`${targetId}_amount`);
			var targetAmountNum = Number(targetAmount.textContent);


			if (targetIsOpen) {
				target.classList.remove('open')
				targetAmount.innerHTML = targetAmountNum - 1
			}

			// when user clicks the trigger 
			var trigger = event.target;
			var triggerId = trigger.getAttribute('id');
			// true if the trigger is already pressed.
			var triggerIsOpen = trigger.classList.contains('open');

			// triggerAmount is the amount it is pressed
			// in the front end this could be either like or dislike amount

			var triggerAmount = document.getElementById(`${triggerId}_amount`);
			// convert the triggerAmount to Number
			var triggerAmountNum = Number(triggerAmount.textContent)


			if (triggerIsOpen) {
				trigger.classList.remove('open')
				// get the number of likes
				triggerAmount.innerHTML = triggerAmountNum - 1
			} else {
				trigger.classList.add('open')
				triggerAmount.innerHTML = triggerAmountNum + 1
			}








		}

	}
	return {
		init
	}

})()

var toggleMenu = {
	// get the nav height 
	// move the menu container by that height
	// display the container
	// create an animation 
	// or just increase the opacity
	navH: function () {
		return document.querySelector('nav').offsetHeight
	},



	toggle: function () {
		var target = document.getElementById('menu-container');
		var isOpen = target.classList.contains('open');


		if (isOpen) {
			// already clicked 
			target.classList.remove('open')
			target.style.top = 0
		} else {
			// not clicked 
			// to toggle 

			// display first 
			target.classList.add('open')
			target.style.top = this.navH() + 'px'


		}
	}


}


// initialize all of the function after the document loaded
document.addEventListener('DOMContentLoaded', function () {
	// call the functions
	toggleOpen.init()
	toggleLike.init()

	document.onscroll = function () {
		var target = document.getElementById('menu-container');
		target.classList.remove('open')


	}






})
window.addEventListener("scroll", function (event) {
	var scrollPos = this.scrollY;
	var far = scrollPos > 100
	var scrollUp = this.oldScroll > this.scrollY
	var target = document.getElementById('sticky-nav')

	if (far && scrollUp) {
		target.classList.add('open')
	} else {
		target.classList.remove('open')
	}


	this.oldScroll = this.scrollY;
});