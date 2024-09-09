document.addEventListener("DOMContentLoaded", function() {
    // Retrieve data from global window object
    const topPersons = window.top_persons || [];
    const topLocations = window.top_locations || [];
    const topOrganizations = window.top_organizations || [];
    const topPersonsLastYear = window.top_persons_last_year || [];
    const topLocationsLastYear = window.top_locations_last_year || [];
    const topOrganizationsLastYear = window.top_organizations_last_year || [];
    
    // Log data for debugging
    console.log("Top Persons:", topPersons);
    console.log("Top Locations:", topLocations);
    console.log("Top Organizations:", topOrganizations);
    console.log("Top Persons Last Year:", topPersonsLastYear);
    console.log("Top Locations Last Year:", topLocationsLastYear);
    console.log("Top Organizations Last Year:", topOrganizationsLastYear);
    
    // Check if data is available and handle empty cases
    function prepareChartData(data) {
        return data.map(item => ({
            k: item._id || item.k,
            v: item.count || item.v
        }));
    }
    
    const personsDataOverall = prepareChartData(topPersons);
    const locationsDataOverall = prepareChartData(topLocations);
    const organizationsDataOverall = prepareChartData(topOrganizations);
    const personsDataLastYear = prepareChartData(topPersonsLastYear);
    const locationsDataLastYear = prepareChartData(topLocationsLastYear);
    const organizationsDataLastYear = prepareChartData(topOrganizationsLastYear);
    
    // Prepare data for charts
    const combinedLabelsOverall = [
        ...personsDataOverall.map(item => item.k),
        ...locationsDataOverall.map(item => item.k),
        ...organizationsDataOverall.map(item => item.k)
    ];
    
    const combinedLabelsLastYear = [
        ...personsDataLastYear.map(item => item.k),
        ...locationsDataLastYear.map(item => item.k),
        ...organizationsDataLastYear.map(item => item.k)
    ];
    
    // Combine and sort data by label for overall chart
    const combinedDataOverall = combinedLabelsOverall.reduce((acc, label) => {
        acc[label] = {
            persons: 0,
            locations: 0,
            organizations: 0
        };
        return acc;
    }, {});
    
    personsDataOverall.forEach(item => combinedDataOverall[item.k].persons = item.v);
    locationsDataOverall.forEach(item => combinedDataOverall[item.k].locations = item.v);
    organizationsDataOverall.forEach(item => combinedDataOverall[item.k].organizations = item.v);
    
    const overallDataPersons = combinedLabelsOverall.map(label => combinedDataOverall[label].persons);
    const overallDataLocations = combinedLabelsOverall.map(label => combinedDataOverall[label].locations);
    const overallDataOrganizations = combinedLabelsOverall.map(label => combinedDataOverall[label].organizations);
    
    // Combine and sort data by label for last year chart
    const combinedDataLastYear = combinedLabelsLastYear.reduce((acc, label) => {
        acc[label] = {
            persons: 0,
            locations: 0,
            organizations: 0
        };
        return acc;
    }, {});
    
    personsDataLastYear.forEach(item => combinedDataLastYear[item.k].persons = item.v);
    locationsDataLastYear.forEach(item => combinedDataLastYear[item.k].locations = item.v);
    organizationsDataLastYear.forEach(item => combinedDataLastYear[item.k].organizations = item.v);
    
    const lastYearDataPersons = combinedLabelsLastYear.map(label => combinedDataLastYear[label].persons);
    const lastYearDataLocations = combinedLabelsLastYear.map(label => combinedDataLastYear[label].locations);
    const lastYearDataOrganizations = combinedLabelsLastYear.map(label => combinedDataLastYear[label].organizations);

    // Log data for debugging
    console.log("Combined Labels Overall:", combinedLabelsOverall);
    console.log("Overall Data Persons:", overallDataPersons);
    console.log("Overall Data Locations:", overallDataLocations);
    console.log("Overall Data Organizations:", overallDataOrganizations);
    console.log("Combined Labels Last Year:", combinedLabelsLastYear);
    console.log("Last Year Data Persons:", lastYearDataPersons);
    console.log("Last Year Data Locations:", lastYearDataLocations);
    console.log("Last Year Data Organizations:", lastYearDataOrganizations);
    
    // Initialize Overall Top Keywords Chart
    const overallCtx = document.getElementById('topKeywordsOverallChart').getContext('2d');
    new Chart(overallCtx, {
        type: 'bar',
        data: {
            labels: combinedLabelsOverall,
            datasets: [
                {
                    label: 'Persons',
                    data: overallDataPersons,
                    backgroundColor: 'blue',
                    stack: 'stack0'
                },
                {
                    label: 'Locations',
                    data: overallDataLocations,
                    backgroundColor: 'green',
                    stack: 'stack1'
                },
                {
                    label: 'Organizations',
                    data: overallDataOrganizations,
                    backgroundColor: 'red',
                    stack: 'stack2'
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    stacked: true,
                    title: { display: true, text: 'Keywords' }
                },
                y: {
                    stacked: true,
                    title: { display: true, text: 'Count' }
                }
            }
        }
    });
    
    // Initialize Last Year Top Keywords Chart
    const lastYearCtx = document.getElementById('topKeywordsLastYearChart').getContext('2d');
    new Chart(lastYearCtx, {
        type: 'bar',
        data: {
            labels: combinedLabelsLastYear,
            datasets: [
                {
                    label: 'Persons',
                    data: lastYearDataPersons,
                    backgroundColor: 'blue',
                    stack: 'stack0'
                },
                {
                    label: 'Locations',
                    data: lastYearDataLocations,
                    backgroundColor: 'green',
                    stack: 'stack1'
                },
                {
                    label: 'Organizations',
                    data: lastYearDataOrganizations,
                    backgroundColor: 'red',
                    stack: 'stack2'
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    stacked: true,
                    title: { display: true, text: 'Keywords' }
                },
                y: {
                    stacked: true,
                    title: { display: true, text: 'Count' }
                }
            }
        }
    });
});
