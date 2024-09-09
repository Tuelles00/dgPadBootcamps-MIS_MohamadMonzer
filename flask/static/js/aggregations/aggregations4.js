document.addEventListener('DOMContentLoaded', function() {
    // Global variables for data
    let articles_in_2024_08_10 = window.articles_in_2024_08_10;
    let articles_published_last_hour = window.articles_published_last_hour;
    let articles_with_more_than_500_and_more_than_600_words = window.articles_with_more_than_500_and_more_than_600_words;
    let count_Israel_hamas_word = window.count_Israel_hamas_word;
    let top_10_most_updated_by_title = window.top_10_most_updated_by_title;

    function renderCharts() {
        // Chart for articles_in_2024_08_10
        Highcharts.chart('container1', {
            chart: { type: 'bar' },
            title: { text: 'Articles on 2024-08-10' },
            xAxis: {
                categories: articles_in_2024_08_10.map(item => item.date),
                title: { text: 'Date' }
            },
            yAxis: {
                min: 0,
                title: { text: 'Number of Articles' }
            },
            series: [{ name: 'Articles', data: articles_in_2024_08_10.map(item => item.count) }]
        });

        // Populate the table for articles_published_last_hour
        const tableBody = document.getElementById('articlesTable').getElementsByTagName('tbody')[0];
        tableBody.innerHTML = ''; // Clear existing rows

        articles_published_last_hour.forEach(item => {
            const row = tableBody.insertRow();
            const cell1 = row.insertCell(0);
            const cell2 = row.insertCell(1);
            // Correctly parse and format the date
            const publishedTime = new Date(item.published_time);
            cell1.textContent = publishedTime.toLocaleString(); // Convert timestamp to readable date
            cell2.textContent = item.title; // Use the title from the JSON
        });

        // Check if data is available for articles_with_more_than_500_and_more_than_600_words
        if (articles_with_more_than_500_and_more_than_600_words.length === 0) {
            document.getElementById('container3').style.display = 'none';
            document.getElementById('no-data-msg3').style.display = 'block';
        } else {
            // Chart for articles_with_more_than_500_and_more_than_600_words
            Highcharts.chart('container3', {
                chart: { type: 'pie' },
                title: { text: 'Articles with More Than 500 and More Than 600 Words' },
                series: [{
                    name: 'Articles',
                    colorByPoint: true,
                    data: [
                        { name: 'More than 500 words', y: articles_with_more_than_500_and_more_than_600_words[0].more_than_500_words },
                        { name: 'More than 600 words', y: articles_with_more_than_500_and_more_than_600_words[0].more_than_600_words }
                    ]
                }]
            });
        }

        // Chart for count_Israel_hamas_word
        Highcharts.chart('container4', {
            chart: { type: 'pie' },
            title: { text: 'Count of Israel and Hamas Words' },
            series: [{
                name: 'Words',
                colorByPoint: true,
                data: Object.entries(count_Israel_hamas_word[0].keyword_counts).map(([keyword, count]) => ({
                    name: keyword,
                    y: count
                }))
            }]
        });

        // Chart for top_10_most_updated_by_title
        Highcharts.chart('container5', {
            chart: { type: 'bar' },
            title: { text: 'Top 10 Most Updated by Title' },
            xAxis: {
                categories: top_10_most_updated_by_title.map(item => item.title),
                title: { text: 'Title' }
            },
            yAxis: {
                min: 0,
                title: { text: 'Update Count' }
            },
            series: [{ name: 'Updates', data: top_10_most_updated_by_title.map(item => item.update_count) }]
        });
    }

    function updateCharts() {
        const date = document.getElementById('dateInput').value;
        if (!date) {
            alert('Please enter a valid date.');
            return;
        }
        // Make an AJAX request to the Flask endpoint
        fetch(`/update_charts/${date}`)
            .then(response => {
                if (response.redirected) {
                    window.location.href = response.url;
                }
            })
            .catch(error => {
                console.error('Error updating charts:', error);
            });
    }

    renderCharts(); // Initial chart rendering
    window.updateCharts = updateCharts; // Expose updateCharts function to global scope
});
