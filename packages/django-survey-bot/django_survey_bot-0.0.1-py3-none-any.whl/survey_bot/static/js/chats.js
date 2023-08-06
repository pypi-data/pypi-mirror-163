$(document).ready(function(){
    var loader = `<i class="fa fa-spin fa-spinner"></i>`
    var csrf_token = $('#csrf-token').val()
    var bot_id = $('#survey-bot-id').val()
    $.ajaxSetup({
        data: { csrfmiddlewaretoken: csrf_token },
    });
    $(document).on('click','.get-chat-data',function(){
        var token = $(this).attr('data-id');
        $('#no_chat_selected_div').hide()
        $('#survey-bot-chatbox').show()
        $.ajax({
            url: $.trim($('#chatbot-chats-url').val()),
            type: "POST",
            data: { bot_id: bot_id,token:token },
            dataType: 'json',
            success: function (response) {
                if (response.hasOwnProperty('status') &&
                    response.status &&
                    response.hasOwnProperty('data') &&
                    response.data) {
                    $('#survey-bot-chatbox').html(response.data.posts_html)
                }
            }
        })
    })
})