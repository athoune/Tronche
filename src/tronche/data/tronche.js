$(function() {
  $.getJSON('domains', null, function(data) {
    var domains = $('#domains');
    $.each(data.domains, function(i, item) {
      var domain = $('<ul>');
      domains.append($('<li>').text(item).click(function(){
        $(this).children().toggle();
      }).append('<div>').append(domain));
      $.getJSON('domain/' + item, null, function(data) {
        $.each(data.sondes, function(i, item) {
          console.log(item);
          domain.append($('<li>').text(item));
        });
      });
    });
  });
});