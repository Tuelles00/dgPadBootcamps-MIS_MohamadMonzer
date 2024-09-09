document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM fully loaded and parsed");

    // Check if dateCountsData exists
    const dateCountsElement = document.getElementById('dateCountsData');
    if (!dateCountsElement) {
        console.error('dateCountsData element not found');
        return;
    }
    
    const dateCounts = JSON.parse(dateCountsElement.textContent);
    console.log("dateCounts:", dateCounts);

    // Prepare data for the chart
    const labels = dateCounts.map(item => item._id);
    const data = dateCounts.map(item => item.count);
    
    // Check if myAreaChart exists
    const ctx = document.getElementById('myAreaChart').getContext('2d');
    if (!ctx) {
        console.error('myAreaChart element not found');
        return;
    }

    // Chart.js configuration
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Number of Articles',
                data: data,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Date'
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Articles'
                    }
                }
            },
            plugins: {
                zoom: {
                    pan: {
                        enabled: true,
                        mode: 'x',
                    },
                    zoom: {
                        enabled: true,
                        mode: 'x',
                        drag: true,
                        speed: 0.1
                    }
                }
            }
        }
    });

    // Add color picker for the line color
    // Create the color picker input element
const colorPicker = document.createElement('input');
colorPicker.type = 'color';
colorPicker.value = '#4BC0C0';

// Assign a class and an ID to the element
colorPicker.className = 'custom-color-picker'; // Add a custom class
colorPicker.id = 'colorPicker'; // Add a unique ID

// Find the navbar container
const navbarContainer = document.querySelector('.navbar-nav.bg-gradient-primary.sidebar.sidebar-dark.accordion');

// Append the color picker inside the navbar
if (navbarContainer) {
    navbarContainer.appendChild(colorPicker);
} else {
    console.error('Navbar container not found');
}

    
    console.log("Color picker added");

    // Update chart color on color change
    colorPicker.addEventListener('input', function(event) {
        const newColor = event.target.value;
        const chart = Chart.getChart(ctx); 
        chart.data.datasets[0].borderColor = newColor;
        chart.data.datasets[0].backgroundColor = newColor + '33';
        chart.update();
        console.log("Chart color updated to:", newColor);
    });
});
