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

// #レスポンシブ対応
$(document).ready(function(){
if (window.matchMedia( '(min-width: 320px) and (max-width: 639px)' ).matches) {
  viewportWidth = 270
  viewportHeight = 170
  boundaryWidth = 290
  boundaryHeight = 180
} else if (window.matchMedia( '(min-width: 640px) and (max-width: 1023px)' ).matches) {
  viewportWidth = 460
  viewportHeight = 290
  boundaryWidth = 480
  boundaryHeight = 290
} else {
  viewportWidth = 650
  viewportHeight = 400
  boundaryWidth = 700
  boundaryHeight = 400
}

// #croppieの初期設定
$image_crop = $('#image_demo').croppie({
 enableExif: true,
  viewport: {
   width: viewportWidth,
   height:viewportHeight,
   type:'square' //circle
  },
  boundary: {
   width: boundaryWidth,
   height: boundaryHeight
  }
});

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
  beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
  }
});

$('#upload_image').on('change', function(){
  var reader = new FileReader();
  reader.onload = function (event) {
    $image_crop.croppie('bind', {
    url: event.target.result
   }).then(function(){
     console.log('jQuery bind complete');
   });
 }
 reader.readAsDataURL(this.files[0]);
  $('#uploadimageModal').addClass('show');
  $('#uploadimageModal').css('display','block');
});

// #ボタンをクリックしたら
$('.crop_image').click(function(event){
 $image_crop.croppie('result', {
   type: 'canvas',
   size: 'viewport'
 }).then(function(response){
  //  console.log(response)
   $.ajax({
     url: '',
     type: "POST",
     data:{"image": response},
     success:function(data) {  
      $('#uploadimageModal').removeClass('show');
      $('#uploadimageModal').css('display','none');
      $('input[type=file]').val('');　//inputファイルを空にする。
      $('#ajax_account_image').attr('src',data.image);
      setTimeout(function(){
        $("#overlay").fadeOut(300);
      },500);
     }
   });
  })
 });

// #モーダル を閉じる
$(document).ready(function(){
  $('#croppie_close').click(function() {
    $('#uploadimageModal').removeClass('show');
    $('#uploadimageModal').css('display','none');
    $('input[type=file]').val('');
  });
});
  });