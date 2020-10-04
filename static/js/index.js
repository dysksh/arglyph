$(function(){
  $('.btn-trigger').on('click', function() {
    $(this).toggleClass('active');
    $('.menu_wrapper').toggleClass('active');
    return false;
  });
});