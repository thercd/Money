$(function(){
    $(document).on( 'click','.remover', function(){
        var remover_box = $(this).parent().find('.remover-cb')[0]
        $(remover_box).prop('checked', true);
        $(this).parent().parent().hide();
    } );

    eventoCbox();
    $('#add_more').click(function() {
        var maximo_forms = $('#id_form-MAX_NUM_FORMS').val();
        var quantidade_forms = $('.remover-cb:not(":checked")').length;
        if (quantidade_forms < maximo_forms){
            var form_idx = $('#id_form-TOTAL_FORMS').val();
            $('#forms').append($('#empty_form').html().replace(/__prefix__/g, form_idx));
            $('#id_form-TOTAL_FORMS').val(parseInt(form_idx) + 1);
            reloadSemantic();
        }else{
            alert('Nao pode mais');
        }
    });
})

function reloadSemantic(){
    $('.ui.dropdown').dropdown();
    eventoCbox();
}
function eventoCbox(){
    $('.checkbox').checkbox({
            onChecked: function () {
//            $(".periodos").removeClass('disabled');
//            $(".periodos").addClass('required');
    },
            onUnchecked: function () {
//             $(".periodos").addClass('disabled');
//             $(".periodos").removeClass('required');
            }
    });
}