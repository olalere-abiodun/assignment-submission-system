  $(document).ready(function () {
    const $themeButtons = $('[data-bs-theme-value]');
    const $html = $('html');

    $themeButtons.on('click', function () {
      const theme = $(this).data('bs-theme-value');

      // Set theme on <html>
      $html.attr('data-bs-theme', theme);

      // Update active and aria-pressed states
      $themeButtons
        .removeClass('active')
        .attr('aria-pressed', 'false');

      $(this)
        .addClass('active')
        .attr('aria-pressed', 'true');
    });
  });

