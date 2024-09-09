document.addEventListener("DOMContentLoaded", function() {
    // Check if data is available
    var dataAvailable = window.articles.length > 0; // Assuming articles is available on the window object

    if (dataAvailable) {
        // Hide loading spinner and show main content
        document.getElementById('loadingSpinner').style.display = 'none';
        document.getElementById('loadingText').style.display = 'none';
        document.getElementById('mainContent').style.display = 'block';

        // Prepare data for the Chart.js chart
        var labels = [];
        var data = [];

        window.articles.forEach(function(article) {
            labels.push(article.published_time);
            data.push(article.sentiment.score);
        });

        var ctx = document.getElementById('sentimentChart').getContext('2d');
        var sentimentChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Sentiment Score',
                    data: data,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Published Time'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Sentiment Score'
                        },
                        suggestedMin: 0,
                        suggestedMax: 1
                    }
                }
            }
        });
    } else {
        // Show loading spinner
        document.getElementById('loadingSpinner').style.display = 'block';
        document.getElementById('loadingText').style.display = 'block';

        // Optionally, reload the page after some time to check for new data
        setTimeout(function() {
            location.reload();
        }, 5000); // Refresh every 5 seconds
    }
});
