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

  var $header = $('#default-header');
  if ($header.length < 1) {
    return;
  }

  setTimeout(function () {
    $header.addClass('stage-1');
  }, 2000);

  setTimeout(function () {
    $header.addClass('stage-2');
  }, 4000);

});
