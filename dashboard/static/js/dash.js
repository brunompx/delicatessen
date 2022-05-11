

// function getPieChartData(productId, action) {
// 	var url = '/order_update_item/'
// 	fetch(url, {
// 		method:'POST',
// 		headers:{
// 			'Content-Type':'application/json',
// 			'X-CSRFToken':csrftoken,
// 		}, 
// 		body:JSON.stringify({'fromDate':fromDate, 'toDate':toDate})
// 	})
// 	.then((resp) => { return resp.json(); })
// 	.then((data) => {
// 		displayPieChart()
// 	});
// }


// Pie Chart
function displayPieChart(pieData, pieLabels) {

    console.log(pieData);
    console.log(pieLabels);

    var ctx = document.getElementById("pieChart");
    var customPieChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: pieLabels,
            datasets: [{
                data: pieData,
                backgroundColor: randomColorsForChart(pieData.length),
                hoverBackgroundColor: randomColorsForChart(pieData.length),
                hoverBorderColor: "rgba(234, 236, 244, 1)",
            }],
        },
        options: {
            maintainAspectRatio: false,
            tooltips: {
                backgroundColor: "rgb(255,255,255)",
                bodyFontColor: "#858796",
                borderColor: '#dddfeb',
                borderWidth: 1,
                xPadding: 15,
                yPadding: 15,
                displayColors: false,
                caretPadding: 10,
            },
            legend: {
                display: true,
                position: 'bottom',
            },
            cutoutPercentage: 70,
            plugins: {
                datalabels: {
                    display: true,
                    formatter: (value) => {
                        return value + '%';
                    }
                }
            },
        },
    });
}

// Line Chart
function displayLineChart(lineData, lineLabels) {
    var ctx = document.getElementById("lineChart");
    var customLineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: lineLabels,
            datasets: [{
                label: "Quantity",
                lineTension: 0.3,
                backgroundColor: "rgba(78, 115, 223, 0.05)",
                borderColor: "#f56038",
                pointRadius: 3,
                pointBackgroundColor: "#f7a325",
                pointBorderColor: "#f56038",
                pointHoverRadius: 3,
                pointHoverBackgroundColor: "#f56038",
                pointHoverBorderColor: "#f7a325",
                pointHitRadius: 10,
                pointBorderWidth: 2,
                data: lineData,
            }],
        },
        options: {
            maintainAspectRatio: false,
            layout: {
            padding: {
                left: 10,
                right: 25,
                top: 25,
                bottom: 0
            }
            },
            scales: {
                xAxes: [{
                    time: {
                        unit: 'date'
                    },
                    gridLines: {
                        display: false,
                        drawBorder: false
                    },
                    ticks: {
                        maxTicksLimit: 7
                    }
                }],
                yAxes: [{
                    ticks: {
                        maxTicksLimit: 5,
                        padding: 10,
                        // Include a dollar sign in the ticks
                        callback: function(value, index, values) {
                            return number_format(value);
                        }
                    },
                    gridLines: {
                        color: "rgb(234, 236, 244)",
                        zeroLineColor: "rgb(234, 236, 244)",
                        drawBorder: false,
                        borderDash: [2],
                        zeroLineBorderDash: [2]
                    }
                }],
            },
            legend: {
                display: false
            },
            tooltips: {
                backgroundColor: "rgb(255,255,255)",
                bodyFontColor: "#858796",
                titleMarginBottom: 10,
                titleFontColor: '#6e707e',
                titleFontSize: 14,
                borderColor: '#dddfeb',
                borderWidth: 1,
                xPadding: 15,
                yPadding: 15,
                displayColors: false,
                intersect: false,
                mode: 'index',
                caretPadding: 10,
                callbacks: {
                    label: function(tooltipItem, chart) {
                        var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
                        return datasetLabel + ': ' + number_format(tooltipItem.yLabel);
                    }
                }
            }
        }
    });
}

function randomColorsForChart(count) {
    var colors = ["#12492f","#0a2f35","#f56038","#f7a325","#ffca7a","#543c52","#f55951","#edd2cb","#361d32"];
    var ranColors = [];
    var usedColors = [];
    var previousColor = ""
    while (ranColors.length < count) {
        var ranNumber = Math.floor(Math.random() * 8);
        currentColor = colors[ranNumber];
        if (currentColor != previousColor) {
            if (usedColors.length < colors.length) {
                if (!usedColors.includes(currentColor)) {
                    ranColors.push(currentColor);
                    usedColors.push(currentColor);
                    previousColor = currentColor
                }
            } else {
                ranColors.push(currentColor);
                previousColor = currentColor
            }
        }
    }
    return ranColors;
}

function number_format(number, decimals, dec_point, thousands_sep) {
    // *     example: number_format(1234.56, 2, ',', ' ');
    // *     return: '1 234,56'
    number = (number + '').replace(',', '').replace(' ', '');
    var n = !isFinite(+number) ? 0 : +number,
      prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
      sep = (typeof thousands_sep === 'undefined') ? ',' : thousands_sep,
      dec = (typeof dec_point === 'undefined') ? '.' : dec_point,
      s = '',
      toFixedFix = function(n, prec) {
        var k = Math.pow(10, prec);
        return '' + Math.round(n * k) / k;
      };
    // Fix for IE parseFloat(0.55).toFixed(0) = 0;
    s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.');
    if (s[0].length > 3) {
      s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
    }
    if ((s[1] || '').length < prec) {
      s[1] = s[1] || '';
      s[1] += new Array(prec - s[1].length + 1).join('0');
    }
    return s.join(dec);
  }