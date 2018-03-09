$(document).ready(function() {
  $(document).on('click', '[data-href]:not(a)', function() {
    window.location = $(this).attr('data-href');
  });
});
