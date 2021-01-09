$(document).ready(function () {
  $('#add').click(function (e) {
    e.prevetDefault();
    $('#members').append(
      '<div><input type="text" name="member" /><button><i class="fas fa-minus"></i></button></div>'
    );
  });

  $('#delete').click(function (e) {
    $(this).parent('div').remove();
  });
});
