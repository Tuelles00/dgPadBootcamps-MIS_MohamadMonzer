// static/js/search.js

function searchInPage() {
    const searchTerm = document.getElementById('searchInput').value.trim();
    if (searchTerm === '') return false;  // Don't search if input is empty

    const content = document.body.innerHTML;  // Get the whole content of the page
    const searchRegex = new RegExp(`(${searchTerm})`, 'gi');  // Create a regex for searching the term
    
    // Remove existing highlights first
    document.body.innerHTML = content.replace(/<mark class="highlight">(.*?)<\/mark>/gi, '$1');

    // Highlight search term
    const newContent = document.body.innerHTML.replace(searchRegex, `<mark class="highlight">$1</mark>`);
    document.body.innerHTML = newContent;

    return false;  // Prevent default form submission
}
