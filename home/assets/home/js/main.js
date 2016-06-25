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

  // Smooth scrolling for same-page elements
  // Source: http://www.learningjquery.com/2007/10/improved-animated-scrolling-script-for-same-page-links
  $('a[href*="#"]:not([href="#"])').click(function() {
    if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') &&
        location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
      if (target.length) {
        $('html, body').animate({
          scrollTop: target.offset().top
        }, 1000);
        return false;
      }
    }
  });

  var $header = $('#default-header');
  if ($header.length < 1) {
    return;
  }

  // Home page animation logic
  var homeAnimationDelay = 1000;
  if (Cookies.get('seenHomeAnimation')) {
    homeAnimationDelay = 1000;
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
});
