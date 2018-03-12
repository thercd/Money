$(function(){
    $('#div-periodica').checkbox({
        onChecked: function () {
        $(".periodos").removeClass('disabled'); },
        onUnchecked: function () {
         $(".periodos").addClass('disabled');
        }
    });
    $('#box-rep-anual').checkbox();
})