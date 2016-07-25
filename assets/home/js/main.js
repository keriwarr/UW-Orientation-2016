jQuery(function($) {
  $('.social-feed-container').socialfeed({
    instagram: {
      accounts: ['@mathorientation'],
      limit: 2,
      client_id: '83a26336707148e7ad61db46e8707182',
      access_token: '1679175523.83a2633.d1380d693ce14ea1bd06b926723ca2f7'
    },
    twitter: {
      accounts: ['@MATHorientation'],
      limit: 2,
      consumer_key: 'GeFXep7qANgeRhnAHL1e7D48S',
      consumer_secret: 'xPkEoBe616De9tLcP8Y7pRetc3QMeOFkapnOWvIM6ss8L8ktf9'
    },
    length: 140,
    template: '/assets/home/social-feed-template.html',
    show_media: true
  });

  // Reference: https://chrissilich.com/blog/convert-em-size-to-pixels-with-jquery/
  function em_to_px(input) {
    input = (typeof input == 'number') ? input: parseFloat(input);
    var emSize = parseFloat($("body").css("font-size"));
    return (input * emSize);
  }

  function px_to_em(input) {
    input = (typeof input == 'number') ? input: parseFloat(input);
    var emSize = parseFloat($("body").css("font-size"));
    return (input / emSize);
  }

  // Smooth scrolling for same-page elements
  // Source: http://www.learningjquery.com/2007/10/improved-animated-scrolling-script-for-same-page-links
  $('a[href*="#"]:not([href="#"])').click(function() {
    if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') &&
        location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
      if (target.length) {
        var targetOffset = target.offset().top;
        var additionalOffset = $(this).data('additional-offset');
        var scrollOffset = targetOffset;
        if (additionalOffset && ~additionalOffset.indexOf('em')) {
          console.log(em_to_px(additionalOffset));
          scrollOffset -= em_to_px(additionalOffset);
        } else if (additionalOffset && ~additionalOffset.indexOf('px')) {
          scrollOffset += parseFloat(additionalOffset);
        }

        $('html, body').animate({
          scrollTop: scrollOffset
        }, 1000);
        return false;
      }
    }
  });

  $('.linkify').linkify({
    format: function (value, type) {
      if (type === 'url') {
        value = value.replace(/^(https?:\/\/)?(www\.)?/g, '');
        if (value.length > 50) {
          value = value.slice(0, 50) + '…';
        }
      }
      return value;
    }
  });

  $('time.from-now').each(function (i, time) {
    var $time = $(time);
    $time.text(moment($time.attr('datetime')).fromNow());
  });

  new Konami(function() {
    $('.low-poly svg').remove();
    lowPolyOnLoad({animate: true});
    lowPolyOnResize();
  });

  var $header = $('#default-header');
  if ($header.length < 1) {
    lowPolyOnLoad();
    $(window).resize(lowPolyOnResize);
    return;
  }

  /******** Home page animations *********/

  // This prevents a sudden change in size for the background hero image
  $('#default-header-bg-container').fadeIn(50)

  // Home page animation logic
  var homeAnimationDelay = 1000;
  if (Cookies.get('seenHomeAnimation')) {
    homeAnimationDelay = 0;
    $header.addClass('no-transition')
  }

  setTimeout(function () {
    $header.addClass('stage-1');
  }, 2 * homeAnimationDelay);

  setTimeout(function () {
    $header.addClass('stage-2');
  }, 4 * homeAnimationDelay);

  setTimeout(function () {
    $header.addClass('stage-3');
    Cookies.set('seenHomeAnimation', 'true');
  }, 6 * homeAnimationDelay);


  setTimeout(function () {
    // Disable animation after the initial animation to avoid "laggy" feeling on
    // iOS when the address bar hides during scrolling.
    $header.addClass('no-transition');
  }, 8 * homeAnimationDelay);

  // Make news and social media same size
  $(window).resize(function () {
    var $announcement = $('#home-announcement-body');
    // +2 to account for border
    var targetHeight = Math.max($announcement.height() + 2, 512);
    $('#home-social-feed-bounding').height(targetHeight);
    return true;
  }).trigger('resize');

  // Must happen after the resize event trigger
  lowPolyOnLoad();
  $(window).resize(lowPolyOnResize);
});
