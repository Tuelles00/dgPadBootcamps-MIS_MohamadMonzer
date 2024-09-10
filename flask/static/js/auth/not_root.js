document.addEventListener('DOMContentLoaded', function() {
    // Use the globally defined 'username' variable
    var sidebarLinks = document.querySelectorAll('#accordionSidebar .nav-link, #accordionSidebar .collapse-item');

    sidebarLinks.forEach(function(link) {
        if (username !== 'root') {
            link.classList.add('locked');

            link.addEventListener('mouseover', function(e) {
                alert('Access Denied: You do not have the necessary privileges to access this page.');
            });
        }
    });
});
