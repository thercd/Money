$(function(){
    $('#div-periodica').checkbox({
        onChecked: function () {
        $(".periodos").removeClass('disabled');
        $(".periodos").addClass('required');
},
        onUnchecked: function () {
         $(".periodos").addClass('disabled');
         $(".periodos").removeClass('required');
        }
    });
    $('#box-rep-anual').checkbox();
})