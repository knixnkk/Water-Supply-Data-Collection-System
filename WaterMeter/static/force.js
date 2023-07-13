window.addEventListener('DOMContentLoaded', function() {
    var rotatePrompt = document.getElementById('rotatePrompt');

    function checkOrientation() {
        if (window.innerWidth > window.innerHeight) {
            // Landscape orientation
            rotatePrompt.style.display = 'none';
        } else {
            // Portrait orientation
            rotatePrompt.style.display = 'block';
        }
    }

    // Check the initial orientation
    checkOrientation();

    // Listen for orientation changes
    window.addEventListener('orientationchange', function() {
        checkOrientation();
    });
});