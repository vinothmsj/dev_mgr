function init()
{
/*
   Practically or really i dunno why I put this js.
   It is not being used
*/

$('#login').on('click', function (e) {


    var username = $('#userid').val();
    var password = $('#passwd').val();


});

$('#register').on('click', function (e) {

    var username = $('#reg_userid').val();
    var email = $('#reg_email').val();
    if(email == "")
    {
        alert("Enter a Valid Email");
        return false;
    }
});


};
 $(document).ready(function() {
    init()
 });
