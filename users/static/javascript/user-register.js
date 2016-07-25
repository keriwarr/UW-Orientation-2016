(function(window, teams, $) {
  var picker = null;
  var pickerTimeout = null;

  function attachListeners() {
    var form = $('form');
    form.find('[type="submit"]').on('click', function(ev) {
      ev.preventDefault();
      ev.stopPropagation();
      var data = form.serializeArray();
      var url = window.location.href;
      var self = $(this);
      self.hide();
      $.post(url, data, function(resp, textStatus, jqXHR) {
        if (resp.valid) {
          window.clearTimeout(pickerTimeout);
          pickerShowTeam(resp.team);
          form.find('#reset').show();
        } else {
          alert('Invalid user information.');
          console.log(resp);
          self.show();
        }
      });
    });

    form.find('#reset').on('click', function(ev) {
      var self = $(this);
      self.hide();
      form[0].reset();
      picker.find('p').remove();
      form.find('[type=submit]').show();
      startPicker(300 /* ms */);
    });
  }

  function startPicker(ms) {
    pickerTimeout = window.setTimeout(function() {
      var currentIdx = parseInt(picker.data('index'), 10);
      picker
        .data('index', (currentIdx + 1) % teams.length)
        .find('img')
        .attr('src', teams[(currentIdx + 1) % teams.length]['image']);
      startPicker(ms);
    }, ms);
  }

  function pickerShowTeam(id) {
    for (var i = 0; i < teams.length; i++) {
      var team = teams[i];
      if (team['id'] == id) {
        var p = $('<p/>');
        picker
          .data('index', i)
          .find('img')
          .attr('src', team['image']);
        p
          .css('text-align', 'center')
          .css('margin-bottom', '0px')
          .css('margin-top', '50px')
          .text('Congratulations, you are on team ' + team['name'])
          .prependTo(picker);
        break;
      }
    }
  }

  function attachPicker() {
    var idx = Math.floor((Math.random() * teams.length));
    var $img = $('<img />');
    var $target = $('.page-content').eq(0);
    if (teams.length == 0) {
      return;
    }

    $img
      .css('display', 'block')
      .css('width', 'auto')
      .css('max-width', '100%')
      .css('height', '300px')
      .css('margin', '0 auto')
      .attr('src', teams[idx]['image']);

    picker = $('<div/>');
    picker
      .css('width', '100%')
      .data('index', idx)
      .append($img)
      .appendTo($target);

    startPicker(200 /* ms */);
  }

  $(window).ready(function() {
    attachListeners();
    attachPicker();
  });
})(window, window.TEAMS || [], window.$ || window.jQuery);
