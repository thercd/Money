$(function(){
    $('.message .close')
  .on('click', function() {
    $(this)
      .closest('.message')
      .transition('fade');
  })
;


    $.ajax({
        url : '/despesa/contas/vencidas/',
        type : 'POST',
        success : function(contas){
        var tabela = $('#contas-vencidas');
           if(contas.length > 0){
                var t_body = tabela.append('<tbody></tbody>');
                for(conta in contas){
                    var row = $('<tr></tr>');
                    var dt = new Date(contas[conta]['referente']);
                    row.append('<td>'+contas[conta]['despesa__nome']+'</td>');
                    row.append('<td>'+dt.getUTCDate()+'/'+(dt.getUTCMonth()+1)+'/'+dt.getFullYear()+'</td>');
                    row.append('<td>'+contas[conta]['valor']+'</td>');
                    row.append('<td><button data-conta-id='+contas[conta]['id']+' class="ui blue icon button">  <i class="money bill alternate outline icon"></i></button></td>');
                    t_body.append(row);
                }
           }else{
                tabela.parent().hide();
                $('#alerta-contas-vencidas').toggleClass('hidden visible');

           }
        }
    });

    $(".action").click(function(){
        var action_url = $(this).attr("data-action");
        window.location.href  = action_url
    })
})