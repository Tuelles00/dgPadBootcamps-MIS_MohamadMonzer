 // Get the data from Flask (replace the data with your actual data)
       // var wordCountDistribution = {{ word_count_distribution | tojson }};
        
        // Process the data to get labels and counts
        var labels = wordCountDistribution.map(item => item.range);
        var data = wordCountDistribution.map(item => item.count);
        
        // Set up the pie chart
        var ctx = document.getElementById('myPieChart').getContext('2d');
        var myPieChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#E2E2E2'],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,  // Ensure the chart resizes with the parent container
                maintainAspectRatio: false,  // Allow the chart to change aspect ratio based on container
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    tooltip: {
                        callbacks: {
                            label: function(tooltipItem) {
                                return tooltipItem.label + ': ' + tooltipItem.raw + ' articles';
                            }
                        }
                    }
                }
            }
        });