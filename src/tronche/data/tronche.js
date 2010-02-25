$(function() {
  $.getJSON('domains', null, function(data) {
    var domains = $('#domains');
    $.each(data.domains, function(i, item) {
      var domain = $('<ul class="sondes">');
      domains.append(
        $('<li>')
          .append($('<a href="#">').text(item).click(function(){
            $(this).siblings().toggle();
            return false;
          }))
        .append($('<div>').hide().append(domain))
      );
      $.getJSON('domain/' + item, null, function(data) {
        $.each(data.sondes, function(i, item) {
          console.log(item);
          domain.append($('<li>').text(item));
        });
      });
    });
  });
});