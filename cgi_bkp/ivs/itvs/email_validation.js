$(function(){
  $("#confirm_email").keyup(function(){
    var email = $('#email').val();
    var email_confirmation = $('#confirm_email').val();
    if(email !== email_confirmation) {
      $('#email_error_message').show();
  　} else {
      $('#email_error_message').hide();
    }
  });
});
