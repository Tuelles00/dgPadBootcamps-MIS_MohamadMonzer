document.addEventListener("DOMContentLoaded", function() {
    // Prepare data for the Sentiment Chart
    var sentimentLabels = [];
    var sentimentData = [];
    
    // Use window object to access Flask data passed to JS
    var articles = window.articles || [];
    
    articles.forEach(article => {
        sentimentLabels.push(article.published_time);
        sentimentData.push(article.sentiment.score);
    });

    var ctxSentiment = document.getElementById('sentimentChart').getContext('2d');
    var sentimentChart = new Chart(ctxSentiment, {
        type: 'line',
        data: {
            labels: sentimentLabels,
            datasets: [{
                label: 'Sentiment Score',
                data: sentimentData,
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

    // Prepare data for the Category Chart
    var categoryLabels = [];
    var categoryData = [];

    var categories = window.categories || [];

    categories.forEach(category => {
        categoryLabels.push(category.category);
        categoryData.push(category.count);
    });

    var ctxCategory = document.getElementById('categoryChart').getContext('2d');
    var categoryChart = new Chart(ctxCategory, {
        type: 'bar',
        data: {
            labels: categoryLabels,
            datasets: [{
                label: 'Category Count',
                data: categoryData,
                backgroundColor: 'rgba(153, 102, 255, 0.2)',
                borderColor: 'rgba(153, 102, 255, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Category'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Count'
                    },
                    beginAtZero: true
                }
            }
        }
    });
});
