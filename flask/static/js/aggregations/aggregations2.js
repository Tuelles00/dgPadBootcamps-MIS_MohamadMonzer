document.addEventListener('DOMContentLoaded', function() {
    // Retrieve data from global window object
    const articlesByCoverage = window.articlesByCoverage;
    console.log('Articles by Coverage:', articlesByCoverage);

    const articlesByThumbnailPresence = window.articlesByThumbnailPresence;
    console.log('Articles by Thumbnail Presence:', articlesByThumbnailPresence);

    const mostPopularKeywordsLast7Days = window.mostPopularKeywordsLast7Days;
    console.log('Most Popular Keywords (Last 7 Days):', mostPopularKeywordsLast7Days);

    const articlesGroupedByWordCount = window.articlesGroupedByWordCount;
    console.log('Articles Grouped by Word Count:', articlesGroupedByWordCount);

    const articlesUpdatedAfterPublication = window.articlesUpdatedAfterPublication;
    console.log('Articles Updated After Publication:', articlesUpdatedAfterPublication);

    const articleCountByYear = window.articleCountByYear;
    console.log('Article Count by Year:', articleCountByYear);

    const recentPostData = window.recentPostData;
    console.log('Recent Post Data:', recentPostData);

    const top10PostIdsByLowestWordCount = window.top10PostIdsByLowestWordCount;
    console.log('Top 10 Post IDs by Lowest Word Count:', top10PostIdsByLowestWordCount);

    const top10PostIdsByWordCount = window.top10PostIdsByWordCount;
    console.log('Top 10 Post IDs by Highest Word Count:', top10PostIdsByWordCount);

    // Initialize Highcharts
    Highcharts.chart('coverageChart', {
        chart: {
            type: 'pie'
        },
        title: {
            text: 'Article Coverage'
        },
        series: [{
            name: 'Coverage',
            colorByPoint: true,
            data: articlesByCoverage.map(item => ({
                name: item.coverage || 'Unknown',
                y: item.count
            }))
        }]
    });

    Highcharts.chart('thumbnailChart', {
        chart: {
            type: 'pie'
        },
        title: {
            text: 'Thumbnail Presence'
        },
        series: [{
            name: 'Presence',
            colorByPoint: true,
            data: articlesByThumbnailPresence.map(item => ({
                name: item.thumbnail_presence,
                y: item.count
            }))
        }]
    });

    Highcharts.chart('popularKeywordsChart', {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Popular Keywords (Last 7 Days)'
        },
        xAxis: {
            type: 'category',
            title: {
                text: 'Keywords'
            }
        },
        yAxis: {
            title: {
                text: 'Occurrences'
            }
        },
        series: mostPopularKeywordsLast7Days.map(day => ({
            name: day.date,
            data: day.keyword_counts.map(keyword => ({
                name: keyword.keyword,
                y: keyword.count
            }))
        }))
    });

    Highcharts.chart('wordCountRangeChart', {
        chart: {
            type: 'bar'
        },
        title: {
            text: 'Word Count Range'
        },
        xAxis: {
            type: 'category',
            title: {
                text: 'Word Count'
            }
        },
        yAxis: {
            title: {
                text: 'Number of Articles'
            }
        },
        series: [{
            name: 'Articles',
            data: articlesGroupedByWordCount.map(item => ({
                name: item.word_count,
                y: item.count
            }))
        }]
    });

    Highcharts.chart('updatedAfterPublicationChart', {
        chart: {
            type: 'pie'
        },
        title: {
            text: 'Articles Updated After Publication'
        },
        series: [{
            name: 'Articles',
            colorByPoint: true,
            data: [{
                name: 'Updated',
                y: articlesUpdatedAfterPublication[0].count
            }]
        }]
    });

    Highcharts.chart('articleCountByYearChart', {
        chart: {
            type: 'line'
        },
        title: {
            text: 'Article Count by Year'
        },
        xAxis: {
            categories: articleCountByYear.map(item => item.year),
            title: {
                text: 'Year'
            }
        },
        yAxis: {
            title: {
                text: 'Number of Articles'
            }
        },
        series: [{
            name: 'Articles',
            data: articleCountByYear.map(item => item.count)
        }]
    });

    // Recent Posts Display
    const recentPostsContainer = document.getElementById('recentPosts');
    recentPostData.forEach(post => {
        const postElement = document.createElement('div');
        postElement.className = 'recent-post';
        postElement.innerHTML = `
            <p><strong>Post ID:</strong> ${post.postid}</p>
            <p><strong>Title:</strong> <a href="${post.url}" target="_blank">${post.title}</a></p>
            <p><strong>Keywords:</strong> ${post.keywords.join(', ')}</p>
        `;
        recentPostsContainer.appendChild(postElement);
    });

    // Top 10 Posts by Lowest Word Count
    const topPostsContainer = document.getElementById('topPosts');
    top10PostIdsByLowestWordCount.forEach(post => {
        const postElement = document.createElement('div');
        postElement.className = 'top-post';
        postElement.innerHTML = `
            <p><strong>Post ID:</strong> ${post.postid}</p>
        `;
        topPostsContainer.appendChild(postElement);
    });

    // Top 10 Posts by Highest Word Count
    const topPostsByWordCountContainer = document.getElementById('topPostsByWordCount');
    top10PostIdsByWordCount.forEach(post => {
        const postElement = document.createElement('div');
        postElement.className = 'top-post-by-word-count';
        postElement.innerHTML = `
            <p><strong>Post ID:</strong> ${post.postid}</p>
        `;
        topPostsByWordCountContainer.appendChild(postElement);
    });
});
