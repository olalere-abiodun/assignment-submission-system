$('button').hover(function() {
    $(this).addClass('btn-hover');
}, function() {
    $(this).removeClass('btn-hover');
});

$('.sign-btn').click(function () {
  $('#fullscreen-spinner').removeClass('hidden'); // Show spinner

  // Redirect after short delay (optional)
  setTimeout(function () {
    window.location.href = './signup.html';
  }, 1000); // Give the spinner a brief moment to appear
});

$('.login-btn').click(function () {
  $('#fullscreen-spinner').removeClass('hidden'); // Show spinner

  // Redirect after short delay (optional)
  setTimeout(function () {
    window.location.href = './login.html';
  }, 1000); // Give the spinner a brief moment to appear
});





