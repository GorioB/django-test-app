$.validator.addMethod('phone', function(value, element) {
  return this.optional(element) || /^[0-9\-\(\) \+]+$/.test(value);
}, "Only numbers, (, ), -, +, and spaces are allowed.");

$.validator.addMethod('range_digits', function(value, element, params) {
  var count = 0;
  value.split('').forEach(function(letter) {
    if (!isNaN(parseInt(letter))) {
      count++;
    }
  });

  return (count >= params[0] && count <= params[1]);
}, function(params, element) {
  return 'Phone number must contain ' + params[0] + '-' + params[1] + ' digits'
});

$('form').validate({
  rules: {
    email_address: {
      required: true,
      maxlength: 254
    },
    phone_number: {
      required: true,
      maxlength: 20,
      phone: true,
      range_digits: [7, 15]
    },
    my_property_type: {
      required: true
    },
    notes: {
      minlength: 10
    }
  }
});

$('#button-id-submit').click(function() {
  var form = $('form');
  if ($(form).valid()) {
    $('input[type="button"]').button('loading');
    $.ajax({
      method: 'post',
      url: url,
      data: $(form).serialize()
    }).done(function(r) {
      if (r.success) {
        $('.alert-area').html(
          "<div class='alert alert-success alert-dismissable'>" +
          "<a href='#' class='close' data-dismiss='alert'>x</a>" +
          "<strong>Form submitted successfuly!</strong>" +
          "</div>"
        );
        $('form').trigger('reset');
      } else {
        var errors_list = $('<ul>');
        for (var key in r.error) {
          var sub_errors = $('<ul>');
          var value = r.error[key]
          value.forEach(function(e){
            $(sub_errors).append("<li>").text(e);
          });
          var error_list_item = $('<li>').text(key).append(sub_errors);
          $(errors_list).append(error_list_item);
        }

        $('.alert-area').html(
          "<div class='alert alert-danger alert-dismissable'>" +
          "<a href='#' class='close' data-dismiss='alert'>x</a>" +
          "<strong>Error submitting form!</strong>" +
          "<p>" + errors_list.html() + "</p>" +
          "</div>"
        );
      }
    }).fail(function() {
      $('.alert-area').html(
        "<div class='alert alert-danger alert-dismissable'>" +
        "<a href='#' class='close' data-dismiss='alert'>x</a>" +
        "<strong>Error communicating with server.</strong>" +
        "</div>"
      );
    }).always(function() {
      $(document).scrollTop(0);
      $('input[type="button"]').button('reset');
    });
  }

});
