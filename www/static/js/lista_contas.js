$(function(){
    $(".action").click(function(){
        var action_url = $(this).attr("data-action");
        window.location.href  = action_url
    })
})