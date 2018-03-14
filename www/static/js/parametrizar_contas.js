$(function(){
    $('.data-pagamento').transition('hide');
    var maximo_forms = $('#id_form-MAX_NUM_FORMS').val();
    $('#maximo-formularios').text(maximo_forms);
    $(document).on( 'click','.remover', function(){
        var remover_box = $(this).parent().find('.remover-cb')[0]
        $(remover_box).prop('checked', true);
        $(this).parent().parent().hide();
        if($("#alerta-maximo-formularios").hasClass("visible")){
            $("#alerta-maximo-formularios").addClass("hidden");
            $("#alerta-maximo-formularios").removeClass("visible");
        }
         $().toggleClass('visible hidden');
    } );

    eventoCbox();
    $('#add_more').click(function() {
        var quantidade_forms = $('.remover-cb:not(":checked")').length;
        if (quantidade_forms < maximo_forms){
            var form_idx = $('#id_form-TOTAL_FORMS').val();
            $('#forms').append($('#empty_form').html().replace(/__prefix__/g, form_idx));
            $('#id_form-TOTAL_FORMS').val(parseInt(form_idx) + 1);
            reloadSemantic();
        }else{
            if($("#alerta-maximo-formularios").hasClass("hidden")){
                $("#alerta-maximo-formularios").removeClass("hidden");
                $("#alerta-maximo-formularios").addClass("visible");
            }
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
                var cb = $(this);
                var div_data_pagamento = cb.parent().parent().parent().parent().find('.data-pagamento')[0];
                $(div_data_pagamento).transition('hide');
                $(div_data_pagamento).transition('horizontal flip', '500ms')
    },
            onUnchecked: function () {
                var cb = $(this);
                var div_data_pagamento = cb.parent().parent().parent().parent().find('.data-pagamento')[0];
                $(div_data_pagamento).transition('show');
                $(div_data_pagamento).transition('horizontal flip', '500ms')
                $($(div_data_pagamento).find('select')).each(function( index, element ) {
                    console.log(this);
                    $(this).dropdown('clear');
                });
    },
    })
}