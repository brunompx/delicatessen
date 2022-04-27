

function getPieChartData(productId, action) {
	var url = '/order_update_item/'
	fetch(url, {
		method:'POST',
		headers:{
			'Content-Type':'application/json',
			'X-CSRFToken':csrftoken,
		}, 
		body:JSON.stringify({'fromDate':fromDate, 'toDate':toDate})
	})
	.then((resp) => { return resp.json(); })
	.then((data) => {
		displayPieChart()
	});
}


// Pie Chart
function displayPieChart(pieData, pieLabels) {
    var ctx = document.getElementById("myPieChart");
    var myPieChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: pieLabels,
            datasets: [{
                data: pieData,
                backgroundColor: ['#ffca7a', '#f7a325', '#f56038', '#12492f'],
                hoverBackgroundColor: ['#2e59d9', '#17a673', '#12492f', '#2c9faf'],
                hoverBorderColor: "rgba(234, 236, 244, 1)",
            }],
        },
        options: {
            maintainAspectRatio: false,
            tooltips: {
                backgroundColor: "#f7a325",
                bodyFontColor: "#858796",
                borderColor: '#dddfeb',
                borderWidth: 1,
                xPadding: 15,
                yPadding: 15,
                displayColors: false,
                caretPadding: 10,
            },
            legend: {
                display: false
            },
            cutoutPercentage: 80,
        },
    });
}