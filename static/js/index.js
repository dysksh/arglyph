if(performance.navigation.type == 1 && location.hash){
  location.href = location.href.replace(/#.*/, "");
}
$(function(){
  $('.btn-trigger').on('click', function() {
    $(this).toggleClass('active');
    $('.menu_wrapper').toggleClass('active');
    return false;
  });
});

$(function(){
  $('a[href^="#"]').click(function() {
    var speed = 400;
    var href= $(this).attr("href");
    var target = $(href == "#" || href == "" ? 'html' : href);
    var position = target.offset().top;
    $('body,html').animate({scrollTop:position}, speed, 'swing');


    // var id = document.getElementById(href);
    // var urlHash = location.hash;
    $(`${href} .content`).eq(0).css( { 'background-color' : '#f4f5f7' });
    var alertmsg = function(){
      $(`${href} .content`).eq(0).css( { 'background-color' : '#fff' });
    }
    setTimeout(alertmsg, 1500);

    return false;
  });
});