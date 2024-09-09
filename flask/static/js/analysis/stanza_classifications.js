document.addEventListener("DOMContentLoaded", function() {
    const ctx = document.getElementById('chart').getContext('2d');

    // Retrieve data from global window object
    const combinedResults = window.combined_results || [];

    // Initialize datasets for each type
    const data = {
        labels: [], // Categories
        datasets: [
            {
                label: 'Person',
                data: [],
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            },
            {
                label: 'Location',
                data: [],
                backgroundColor: 'rgba(255, 99, 132, 0.6)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            },
            {
                label: 'Organization',
                data: [],
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }
        ]
    };

    // Fill in the data
    combinedResults.forEach(result => {
        if (!data.labels.includes(result.category)) {
            data.labels.push(result.category);
        }

        const categoryIndex = data.labels.indexOf(result.category);

        if (result.value === 'Person') {
            data.datasets[0].data[categoryIndex] = (data.datasets[0].data[categoryIndex] || 0) + 1;
        } else if (result.value === 'Location') {
            data.datasets[1].data[categoryIndex] = (data.datasets[1].data[categoryIndex] || 0) + 1;
        } else if (result.value === 'Organization') {
            data.datasets[2].data[categoryIndex] = (data.datasets[2].data[categoryIndex] || 0) + 1;
        }
    });

    // Render the chart
    new Chart(ctx, {
        type: 'bar',
        data: data,
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});
