$(document).ready(function() {
    const ctx = document.getElementById('sentimentChart').getContext('2d');
    const chartData = window.articles || []; // Retrieve data from global window object

    // Prepare data for chart
    const chartDataset = chartData.map(item => ({
        x: item.postid,
        y: item.overall_sentiment.score,
        backgroundColor: item.overall_sentiment.sentiment === 'positive' ? 'yellow' :
                         item.overall_sentiment.sentiment === 'negative' ? 'red' :
                         'gray',
        borderColor: item.overall_sentiment.sentiment === 'positive' ? 'orange' :
                     item.overall_sentiment.sentiment === 'negative' ? 'darkred' :
                     'darkgray',
        borderWidth: 1,
        sentiment: item.overall_sentiment.sentiment,
        postid: item.postid // Add postid to dataset for use in tooltips
    }));

    const chart = new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Sentiments',
                data: chartDataset,
                backgroundColor: chartDataset.map(item => item.backgroundColor),
                borderColor: chartDataset.map(item => item.borderColor),
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                x: {
                    type: 'category',
                    labels: chartData.map(item => item.postid),
                    title: { display: true, text: 'Post ID' }
                },
                y: { title: { display: true, text: 'Sentiment Score' } }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        title: function(tooltipItems) {
                            // Use the postid in the title of the tooltip
                            return `Post ID: ${tooltipItems[0].raw.postid}`;
                        },
                        label: function(context) {
                            // Use the score in the label of the tooltip
                            return `Score: ${context.raw.y}`;
                        }
                    }
                },
                legend: { display: false }
            }
        }
    });

    // Handle point clicks
    document.getElementById('sentimentChart').addEventListener('click', function(event) {
        const points = chart.getElementsAtEventForMode(event, 'nearest', { intersect: true }, true);
        if (points.length) {
            const index = points[0].index;
            const postId = chartData[index].postid;
            const filename = chartData[index].filename; // Assuming filename is part of chartData
            const overallSentiment = chartData[index].overall_sentiment; // Assuming overall_sentiment is part of chartData
            console.log('Clicked Post ID:', postId);  // Debugging line
            fetch(`/get_post_details?postid=${postId}`)
                .then(response => response.json())
                .then(data => {
                    console.log('Retrieved Data:', data);  // Log the retrieved data
                    $('#details-body').empty();
                    $('#details-body').append(`
                        <tr>
                            <td>${postId}</td>
                            <td>${filename}</td>
                            <td class="${overallSentiment.sentiment}">${overallSentiment.sentiment}</td>
                            <td colspan="3">Overall Sentiment Score: ${overallSentiment.score}</td>
                        </tr>
                    `);
                    if (data.keyword_sentiments && typeof data.keyword_sentiments === 'object') {
                        Object.entries(data.keyword_sentiments).forEach(([keyword, details]) => {
                            $('#details-body').append(`
                                <tr>
                                    <td></td>
                                    <td></td>
                                    <td></td>
                                    <td>${keyword}</td>
                                    <td class="${details.sentiment}">${details.sentiment}</td>
                                    <td>${details.score}</td>
                                </tr>
                            `);
                        });
                        $('#details-table').show();
                    } else {
                        $('#details-body').append('<tr><td colspan="6">No keyword sentiments available</td></tr>');
                        $('#details-table').show();
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    $('#details-body').append('<tr><td colspan="6">Error fetching details</td></tr>');
                    $('#details-table').show();
                });
        }
    });
});
