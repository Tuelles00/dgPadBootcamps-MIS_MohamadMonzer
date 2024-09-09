
let ticker = document.getElementById('news-ticker');
let tickerInterval;  // To store the interval ID for clearing later

// SVG separator
const svgSeparator = `
<svg xmlns="http://www.w3.org/2000/svg" width="20.978" height="11.965" viewBox="0 0 20.978 11.965">
<path id="Path_3236_0" data-name="Path 3236" d="M128.252,661.441a10.466,10.466,0,0,1-3.231.027c-2.172-.27-4.326-.893-6.608-1.088a10.14,10.14,0,0,0-3.488.241,6.622,6.622,0,0,0-3.04,1.776,5.578,5.578,0,0,0-1.616,3.014,4.833,4.833,0,0,0,.623,3.184,7.179,7.179,0,0,0,4.147,3.157,5.015,5.015,0,0,0,3.986-.313,3.673,3.673,0,0,0,1.577-2.011,11.048,11.048,0,0,0,.28-1.08,2.388,2.388,0,0,1,.583-.239c.2.712.511,1.117.934,1.217q.253.063.492-.249a1.355,1.355,0,0,0,.265-.841.783.783,0,0,0-.565-.831q-.33-.061-.658-.1a6.411,6.411,0,0,1-.344-2.122c-.019-.245-.034-.468-.045-.67.267.01.526.013.776,0a5.152,5.152,0,0,0,2.024-.44,3.455,3.455,0,0,0,1.042-.75,3.637,3.637,0,0,0,.282-.336,3.715,3.715,0,0,1-1.71.811,6.082,6.082,0,0,1-1.881.016q-.284-.036-.57-.083a3.7,3.7,0,0,1,.018-.584q.361-.369.3-.516a.52.52,0,0,0-.06-.153,26.021,26.021,0,0,0,3.668.188,8.828,8.828,0,0,0,3.478-.756,5.917,5.917,0,0,0,1.789-1.288,6.244,6.244,0,0,0,.483-.578A6.379,6.379,0,0,1,128.252,661.441Zm-10,9.6a4.928,4.928,0,0,1-3.271-.6,6.41,6.41,0,0,1-2.016-1.647,4.282,4.282,0,0,0,1.415-.14,4.307,4.307,0,0,0,1.889,1.146,2.92,2.92,0,0,0,2.321-.183,2.069,2.069,0,0,0,.568-.507l.111.316-.537.2.313.7.645-.243-.153-.373.574-.158-.289-.7-.644.237a2.266,2.266,0,0,0,.272-.484c.068.007.139.008.214.008.046,0,.092,0,.141,0,.168-.006.356-.043.575-.075.025,0,.077-.021.1-.027A2.8,2.8,0,0,1,118.25,671.042Zm-1.458-3.777a2.525,2.525,0,0,0-.215,1.289c0,.019.008.037.013.055a.847.847,0,0,0,.268.466.572.572,0,0,0,.467.1,1.1,1.1,0,0,0,.133-.028,2.3,2.3,0,0,0,1.152-.9,1.061,1.061,0,0,0,.69.343,1.887,1.887,0,0,1-1.165.8,2.2,2.2,0,0,1-.458.047,3.155,3.155,0,0,1-1.446-.394,3.762,3.762,0,0,1-.924-.681c.154-.06.274-.115.345-.152.629-.325.918-1.613.918-1.613.32-.05.412-.364.738-.537.471-.248.16.246.16.246l-.243.363-.137-.109-.423.6Zm3.743.577a2.073,2.073,0,0,1-.737.088,1.575,1.575,0,0,1-.863-.159,5.473,5.473,0,0,0,.355-.569.1.1,0,0,1,.009-.013c.011-.019.031-.051.048-.085.008-.017.016-.033.023-.05a.122.122,0,0,0,.009-.027.09.09,0,0,0,0-.047c-.012-.049-.024-.1-.037-.142a7.654,7.654,0,0,0-.687-1.739,5,5,0,0,0-.42-.656l-.085-.111-.052.131a.966.966,0,0,0-.06.53l0,.019.011.014a6.451,6.451,0,0,1,.615,1.182,6.516,6.516,0,0,1,.32.8.57.57,0,0,1,.013.062v.008q-.159.255-.317.469a.9.9,0,0,1-.155-.491,1.779,1.779,0,0,1,.013-.276,2.67,2.67,0,0,0-.138.86,1.286,1.286,0,0,0,.028.224,3.653,3.653,0,0,1-.26.273,1.926,1.926,0,0,1-.81.492.327.327,0,0,1-.042.009.462.462,0,0,1-.339-.022.4.4,0,0,1-.174-.266c0-.008,0-.017-.007-.027a1.906,1.906,0,0,1,.031-1.027l.356.282.2-.268.446.351.437-.586-.534-.429-.194.279-.274-.221c.066-.088.147-.2.245-.329,1.106-1.5.06-.92-.171-.776-.207.128-.95.609-1.011.062s-.417.639-.417.639a1.466,1.466,0,0,1,.244,1,8.653,8.653,0,0,1-1.256.57,2.444,2.444,0,0,1-.39-.925l.506.4.437-.587-.534-.429-.413.591a1.571,1.571,0,0,1,.019-.614,2.407,2.407,0,0,1,.8-1.271,2.969,2.969,0,0,1,1.316-.681,9.224,9.224,0,0,1,2.993-.006c.281.031.555.06.826.087.011.2.023.4.031.591A18.292,18.292,0,0,1,120.535,667.843Zm-.082-4.53c-.006.074-.009.149-.011.223a20.29,20.29,0,0,0-2.211-.352,5.868,5.868,0,0,0-2.03.14,3.849,3.849,0,0,0-1.77,1.034,3.246,3.246,0,0,0-.94,1.755,2.8,2.8,0,0,0,.363,1.853c.031.053.065.105.1.156a1.789,1.789,0,0,1-1.309-.19,1.7,1.7,0,0,1-.446-.451,3.074,3.074,0,0,1-.2-1.475l.047-.265a4.133,4.133,0,0,1,1.377-2.183,5.108,5.108,0,0,1,2.26-1.169,15.259,15.259,0,0,1,4.967-.028A3.278,3.278,0,0,0,120.453,663.313Zm.3-.124a3.59,3.59,0,0,1,.063-.811h.011l.119.013,0,0a.848.848,0,0,1,.165.319q.008.5.018.952l-.35-.065C120.761,663.456,120.752,663.32,120.749,663.189Zm.183,4.473c.015-.122-.037-2.64-.085-3.2.091.008.21.024.3.03a26.375,26.375,0,0,0,.192,2.967C121.194,667.529,121.033,667.613,120.932,667.662Zm1.913.912a.647.647,0,0,1-.251.055.45.45,0,0,1-.228-.059.482.482,0,0,1-.3-.49Q122.747,668.053,122.846,668.575Z" transform="translate(-110.21 -660.047)" fill="#ff0505"></path>
</svg>
`;

// Function to calculate the duration for showing all news items
function calculateDisplayTime(newsCount) {
    // Assuming each item takes 5 seconds to display and there is a 2-second pause at the end
    const displayTimePerItem = 5000; // 5 seconds
    const pauseTime = 2000; // 2 seconds
    return (newsCount * displayTimePerItem) + pauseTime;
}

async function fetchNews() {
    try {
        const response = await fetch('/news');
        const newsList = await response.json();

        ticker.innerHTML = ''; // Clear existing ticker content

        newsList.forEach((news, index) => {
            const newsItem = document.createElement('li');
            newsItem.innerHTML = `<a href="${news.link}" target="_blank">${news.title} (${news.date} at ${news.time} - ${news.category})</a>`;
            ticker.appendChild(newsItem);

            // Add SVG separator after each news item except the last one
            if (index < newsList.length - 1) {
                const separator = document.createElement('li');
                separator.innerHTML = svgSeparator;
                ticker.appendChild(separator);
            }
        });

        // Reset the animation
        ticker.style.animation = 'none';
        ticker.offsetHeight;  // Trigger a reflow
        ticker.style.animation = null;

        // Set the ticker animation duration based on the number of items
        const totalDisplayTime = calculateDisplayTime(newsList.length);
        
        // Start a timer to fetch new news after all items have been shown
        if (tickerInterval) clearInterval(tickerInterval); // Clear any previous interval
        tickerInterval = setInterval(() => {
            fetchNews(); // Fetch new news after the calculated time
        }, totalDisplayTime);

    } catch (error) {
        console.error('Error fetching news:', error);
    }
}

// Initial fetch
fetchNews();