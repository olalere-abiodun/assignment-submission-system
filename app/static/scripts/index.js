$('button').hover(function() {
    $(this).addClass('btn-hover');
}, function() {
    $(this).removeClass('btn-hover');
});

$(document).ready(function () {
    // Handle signup button
    $('.sign-btn').click(function () {
      $('#fullscreen-spinner').removeClass('hidden'); // Show spinner

      // Redirect after short delay
      setTimeout(function () {
        window.location.href = '/signup';
      }, 1000);
    });

    // Handle login button
    $('.login-btn').click(function () {
      $('#fullscreen-spinner').removeClass('hidden'); // Show spinner

      // Redirect after short delay
      setTimeout(function () {
        window.location.href = '/login';
      }, 1000);
    });

    // Fix: Hide spinner if returning to the page via browser's back/forward button
    window.addEventListener('pageshow', function () {
      $('#fullscreen-spinner').addClass('hidden'); // Hide spinner on page show
    });
  });





