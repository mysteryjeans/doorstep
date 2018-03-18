$(document).ready(function() {
  $('[data-toggle="tooltip"]').tooltip();
  $(document).on('click', '[data-href]:not(a)', function() {
    window.location = $(this).attr('data-href');
  });
});
