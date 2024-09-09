document.addEventListener("DOMContentLoaded", function() {
    // Retrieve data from global window object
    const trendsAllYears = window.trends_all_years || [];
    const trendsLastYear = window.trends_last_year || [];
    
    // Prepare data for overall trend by year
    const years = trendsAllYears.map(item => item._id);
    const personsByYear = trendsAllYears.map(item => item.persons_count);
    const locationsByYear = trendsAllYears.map(item => item.locations_count);
    const organizationsByYear = trendsAllYears.map(item => item.organizations_count);

    // Prepare data for last year trend by month
    const months = trendsLastYear.map(item => item._id);
    const personsByMonth = trendsLastYear.map(item => item.persons_count);
    const locationsByMonth = trendsLastYear.map(item => item.locations_count);
    const organizationsByMonth = trendsLastYear.map(item => item.organizations_count);

    // Overall Trend Chart
    const overallCtx = document.getElementById('overallTrendChart').getContext('2d');
    new Chart(overallCtx, {
        type: 'line',
        data: {
            labels: years,
            datasets: [
                { label: 'Persons', data: personsByYear, borderColor: 'blue', fill: false },
                { label: 'Locations', data: locationsByYear, borderColor: 'green', fill: false },
                { label: 'Organizations', data: organizationsByYear, borderColor: 'red', fill: false }
            ]
        },
        options: {
            responsive: true,
            scales: {
                x: { title: { display: true, text: 'Year' }},
                y: { title: { display: true, text: 'Count' }}
            }
        }
    });

    // Last Year Trend Chart
    const lastYearCtx = document.getElementById('lastYearTrendChart').getContext('2d');
    new Chart(lastYearCtx, {
        type: 'line',
        data: {
            labels: months,
            datasets: [
                { label: 'Persons', data: personsByMonth, borderColor: 'blue', fill: false },
                { label: 'Locations', data: locationsByMonth, borderColor: 'green', fill: false },
                { label: 'Organizations', data: organizationsByMonth, borderColor: 'red', fill: false }
            ]
        },
        options: {
            responsive: true,
            scales: {
                x: { title: { display: true, text: 'Month' }},
                y: { title: { display: true, text: 'Count' }}
            }
        }
    });
});
