$('form').submit(function(event) {
    $(this).find(':submit').attr("disabled", true);
});
