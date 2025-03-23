//
$(document).ready(function(){
    $('.header_burger,.close_menu').click(function(event) {
        $('.kategor_mob, .back_mob_blaclout,.main_nav_mob_position').toggleClass('active');
        $('body').toggleClass('lock');
    });
   
});

// Footer
  $(document).ready(function(){ 
    $('.nav_footer_one').click(function(event) {
        $('.nav_footer_one').toggleClass('active');
    });
    $('.nav_footer_two').click(function(event) {
      $('.nav_footer_two').toggleClass('active');
    });
    $('.nav_footer_three').click(function(event) {
      $('.nav_footer_three').toggleClass('active');
    });
    $('.nav_footer_four').click(function(event) {
      $('.nav_footer_four').toggleClass('active');
    });
});

$(document).ready(function() {
  
  $('.button-size').on('click', function() {
      $('.button-size').removeClass('is-selected');
      $(this).addClass('is-selected');
  });

  $('.button-check-size').on('click', function() {
      $(this).toggleClass('is-selected');
  });
});

// 
  (function () {
  $(document).ready(function () {
    var $button, $tooltip,$body 
    $button = $('.button_hide_filter')
    $tooltip = $('.sidebar')
    $body = $('body')
    return $button.click(() => {
      if ($tooltip.is(':hidden')) {
        $tooltip.removeAttr('hidden')
        $button.text('Hide Filters')
        $body.addClass("lock_mob")
        $button.attr('aria-expanded', true)
      } else {
        $tooltip.attr('hidden', true)
        $button.text('Show Filters')
        $body.removeClass("lock_mob")
        $button.attr('aria-expanded', false)
      }
    })
  })
}).call(this)


