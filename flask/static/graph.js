window.onload = function() {
    fetch('/get_article_counts')
        .then(response => response.json())
        .then(data => {
            const labels = data.map(item => item.url);
            const counts = data.map(item => item.count);

            const ctx = document.getElementById('articleChart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Number of Articles',
                        data: counts,
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error fetching article counts:', error));
};
