document.addEventListener('DOMContentLoaded', function() {
    am4core.ready(function() {
        // Themes begin
        am4core.useTheme(am4themes_animated);
        // Themes end

        var chart = am4core.create("chartdiv", am4plugins_wordCloud.WordCloud);
        var series = chart.series.push(new am4plugins_wordCloud.WordCloudSeries());

        series.accuracy = 4;
        series.step = 15;
        series.rotationThreshold = 0.7;
        series.maxCount = 200;
        series.minWordLength = 2;
        series.labels.template.margin(4, 4, 4, 4);
        series.maxFontSize = am4core.percent(30);

        // Prepare color palette
        var colorPalette = [
            "#FF5733", "#33FF57", "#3357FF", "#F3FF33", "#FF33A5", "#33FFF8",
            "#FF8C00", "#8A2BE2", "#A52A2A", "#DEB887", "#5F9EA0", "#D2691E",
            "#FF7F50", "#6495ED", "#FFF8DC", "#DC143C", "#00FFFF", "#00008B"
        ];

        // Function to assign colors
        function getColor(index) {
            return colorPalette[index % colorPalette.length];
        }

        // Replace with server-side injected data
        const topKeywords = window.topKeywords;

        // Convert JSON data to a format suitable for the Word Cloud
        var text = topKeywords.map(item => `${item.keyword} `.repeat(item.count)).join(' ');

        // Update the series text
        series.text = text;

        // Apply colors to words
        series.labels.template.adapter.add("fill", function(fill, target) {
            var index = series.dataItems.indexOf(target.dataItem);
            return am4core.color(getColor(index));
        });

        // Add tooltips
        series.tooltip = new am4core.Tooltip();
        series.tooltip.label.interactionsEnabled = true;
        series.tooltip.keepTargetHover = true;

        series.labels.template.tooltipText = "{word}: {count}";
        series.tooltip.getFillFromObject = false;
        series.tooltip.background.fill = am4core.color("#fff");
        series.tooltip.label.fill = am4core.color("#000");

        // Bind data items to the word cloud
        series.data = topKeywords.map(item => ({
            word: item.keyword,
            count: item.count
        }));

        // Update the series' words and counts
        series.dataFields.word = "word";
        series.dataFields.value = "count";

        // Adjust appearance of the tooltips
        series.tooltip.pointerOrientation = "down";
        series.tooltip.background.cornerRadius = 8;
        series.tooltip.background.strokeOpacity = 0;
    }); // end am4core.ready()

    const authorCounts = window.authorCounts;
    const categoryCounts = window.categoryCounts;
    const keywordCounts = window.keywordCounts;
    const languageCounts = window.languageCounts;
    const wordCountSummary = window.wordCountSummary;
    const topAuthor = window.topAuthor;
    const articlesCountsByDate = window.articlesCountsByDate;

    // Function to create a bar chart
    function createBarChart(ctx, labels, data, title) {
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: title,
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
                        beginAtZero: true
                    }
                }
            }
        });
    }

    // Function to create a pie chart
    function createPieChart(ctx, labels, data, title) {
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    label: title,
                    data: data,
                    backgroundColor: [
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(255, 159, 64, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 205, 86, 0.2)'
                    ],
                    borderColor: [
                        'rgba(75, 192, 192, 1)',
                        'rgba(255, 99, 132, 1)',
                        'rgba(255, 159, 64, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 205, 86, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true
            }
        });
    }

    // Function to create a line chart
    function createLineChart(ctx, labels, data, title) {
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: title,
                    data: data,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'day',
                            tooltipFormat: 'll'
                        },
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Count'
                        }
                    }
                }
            }
        });
    }

    // Create charts
    createPieChart(document.getElementById('authorChart').getContext('2d'),
                   authorCounts.map(item => item.author),
                   authorCounts.map(item => item.count),
                   'Author Counts');

    createPieChart(document.getElementById('languageChart').getContext('2d'),
                   languageCounts.map(item => item.lang),
                   languageCounts.map(item => item.count),
                   'Language Counts');

    createBarChart(document.getElementById('categoryChart').getContext('2d'),
                   categoryCounts.map(item => item.category),
                   categoryCounts.map(item => item.count),
                   'Category Counts');

    createBarChart(document.getElementById('topAuthorChart').getContext('2d'),
                   topAuthor.map(item => item.author),
                   topAuthor.map(item => item.count),
                   'Top Authors');

    createBarChart(document.getElementById('topKeywordsChart').getContext('2d'),
                   topKeywords.map(item => item.keyword),
                   topKeywords.map(item => item.count),
                   'Top Keywords');

    createLineChart(document.getElementById('articlesCountsChart').getContext('2d'),
                    articlesCountsByDate.map(item => item.date),
                    articlesCountsByDate.map(item => item.count),
                    'Articles Counts by Date');

    createBarChart(document.getElementById('keywordChart').getContext('2d'),
                   keywordCounts.map(item => item.keyword),
                   keywordCounts.map(item => item.count),
                   'Keyword Counts');

    createBarChart(document.getElementById('wordCountChart').getContext('2d'),
                   wordCountSummary.map(item => item.word_count),
                   wordCountSummary.map(item => item.count),
                   'Word Count Summary');
});
