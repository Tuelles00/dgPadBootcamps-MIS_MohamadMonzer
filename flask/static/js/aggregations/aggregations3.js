// Ensure the amCharts core is ready before executing the script
am4core.ready(function() {
    // Get the data passed from Flask
    var chartData1 = window.chartData1;
    var chartData2 = window.chartData2;
    var chartData3 = window.chartData3;
    var chartData4 = window.chartData4;
    var chartData5 = window.chartData5;

    // Create chart instance for articles_100_200_specific
    var chart1 = am4core.create("chartdiv", am4charts.XYChart);
    chart1.data = chartData1;

    var categoryAxis1 = chart1.xAxes.push(new am4charts.CategoryAxis());
    categoryAxis1.dataFields.category = "word_count";
    categoryAxis1.title.text = "Word Count";

    var valueAxis1 = chart1.yAxes.push(new am4charts.ValueAxis());
    valueAxis1.title.text = "Count";

    var series1 = chart1.series.push(new am4charts.ColumnSeries());
    series1.dataFields.valueY = "count";
    series1.dataFields.categoryX = "word_count";
    series1.name = "Count";
    series1.columns.template.tooltipText = "{categoryX}: [bold]{valueY}[/]";
    series1.columns.template.fillOpacity = 0.8;
    series1.columns.template.strokeOpacity = 0;

    chart1.cursor = new am4charts.XYCursor();
    chart1.legend = new am4charts.Legend();

    // Create chart instance for articles_by_count_range_min_max
    var chart2 = am4core.create("chartdiv2", am4charts.XYChart);
    chart2.data = chartData2[0];

    var categoryAxis2 = chart2.yAxes.push(new am4charts.CategoryAxis());
    categoryAxis2.dataFields.category = "range";
    categoryAxis2.title.text = "Count Range";

    var valueAxis2 = chart2.xAxes.push(new am4charts.ValueAxis());
    valueAxis2.title.text = "Count";

    var series2 = chart2.series.push(new am4charts.ColumnSeries());
    series2.dataFields.valueX = "count";
    series2.dataFields.categoryY = "range";
    series2.name = "Count";
    series2.columns.template.tooltipText = "{categoryY}: [bold]{valueX}[/]";
    series2.columns.template.fillOpacity = 0.8;
    series2.columns.template.strokeOpacity = 0;
    series2.columns.template.column.cornerRadiusTopLeft = 5;
    series2.columns.template.column.cornerRadiusTopRight = 5;

    chart2.cursor = new am4charts.XYCursor();
    chart2.legend = new am4charts.Legend();

    // Prepare data for articles_by_length_of_titles
    var lengthOfTitlesData = chartData3.map(item => ({
        length: item.articles[0].title_length,
        count: item.count
    }));

    var chart3 = am4core.create("chartdiv3", am4charts.XYChart);
    chart3.data = lengthOfTitlesData;

    var categoryAxis3 = chart3.xAxes.push(new am4charts.CategoryAxis());
    categoryAxis3.dataFields.category = "length";
    categoryAxis3.title.text = "Title Length";

    var valueAxis3 = chart3.yAxes.push(new am4charts.ValueAxis());
    valueAxis3.title.text = "Count";

    var series3 = chart3.series.push(new am4charts.ColumnSeries());
    series3.dataFields.valueY = "count";
    series3.dataFields.categoryX = "length";
    series3.name = "Count";
    series3.columns.template.tooltipText = "{categoryX}: [bold]{valueY}[/]";
    series3.columns.template.fillOpacity = 0.8;
    series3.columns.template.strokeOpacity = 0;

    chart3.cursor = new am4charts.XYCursor();
    chart3.legend = new am4charts.Legend();

    // Prepare data for articles_by_month
    var formattedData = chartData4.map(item => ({
        date: `${item.year}/${item.month.toString().padStart(2, '0')}`,
        count: item.count
    }));

    // Create the chart instance for articles_by_month
    var chart4 = am4core.create("chartdiv4", am4charts.XYChart);
    chart4.data = formattedData;

    // Create and configure the x-axis
    var categoryAxis4 = chart4.xAxes.push(new am4charts.CategoryAxis());
    categoryAxis4.dataFields.category = "date";
    categoryAxis4.title.text = "Year/Month";
    categoryAxis4.renderer.labels.template.rotation = -45; // Rotate labels for better readability
    categoryAxis4.renderer.labels.template.horizontalCenter = "right";
    categoryAxis4.renderer.labels.template.verticalCenter = "middle";
    categoryAxis4.renderer.labels.template.dy = 10; // Adjust vertical position

    // Create and configure the y-axis
    var valueAxis4 = chart4.yAxes.push(new am4charts.ValueAxis());
    valueAxis4.title.text = "Count";

    // Create and configure the series
    var series4 = chart4.series.push(new am4charts.ColumnSeries());
    series4.dataFields.valueY = "count";
    series4.dataFields.categoryX = "date";
    series4.name = "Count";
    series4.columns.template.tooltipText = "{categoryX}: [bold]{valueY}[/]";
    series4.columns.template.fillOpacity = 0.8;
    series4.columns.template.strokeOpacity = 0;

    // Add a cursor
    chart4.cursor = new am4charts.XYCursor();
    chart4.legend = new am4charts.Legend();

    // Create chart instance for articles_grouped_by_Coverage
    var chart5 = am4core.create("chartdiv5", am4charts.PieChart);
    chart5.data = chartData5;

    var pieSeries = chart5.series.push(new am4charts.PieSeries());
    pieSeries.dataFields.value = "count";
    pieSeries.dataFields.category = "coverage";
    pieSeries.slices.template.tooltipText = "{category}: [bold]{value}[/]";
    pieSeries.slices.template.fillOpacity = 0.8;

    chart5.legend = new am4charts.Legend();
});
