$(function(){
    var checkbox_pagamento = null;
    $('.ui.dropdown').dropdown();
    $('.step-1').addClass('completed');
    $('.step-2').addClass('active');

    $( ".valor-change" ).change(function() {
        var input = $('#'+$(this).attr('data-valor-id'));
        input.val($(this).val());
    });

    $('.checkbox').checkbox({
        onChecked: function () {
            checkbox_pagamento = $(this).parent();
            $('.ui.basic.modal')
                .modal({
            closable  : false,
            onDeny    : function(){
                $(checkbox_pagamento).checkbox('uncheck');
            },
            onApprove : function() {
            var data_pg = $('#data-pagamento');
                if( data_pg.val() == ""){
                    alert('Data de pagamento pendente');
                    return false;
                }else{
                    var input_dt = $(checkbox_pagamento).attr('data-dt-paga-id');
                    $('#'+input_dt).val(data_pg.val());
                    var cb_id = $(checkbox_pagamento).attr('data-paga-id');
                    $('#'+cb_id).prop('checked', true);
                    var dt = new Date(data_pg.val());
                    $(checkbox_pagamento).parent().next().text(dt.getUTCDate()+'/'+(dt.getUTCMonth()+1)+'/'+dt.getFullYear());
                    checkbox_pagamento = null;
                    data_pg.val('');
                }
            }
            }).modal('show');
        },
        onUnchecked: function () {
            var cb = $(this).parent();
            var input_dt = $(cb).attr('data-dt-paga-id');
            $('#'+input_dt).val($('#data-pagamento').val());
            var cb_id = $(cb).attr('data-paga-id');
            $('#'+cb_id).prop('checked', false);
            cb.parent().next().text('');
        },
    })
})