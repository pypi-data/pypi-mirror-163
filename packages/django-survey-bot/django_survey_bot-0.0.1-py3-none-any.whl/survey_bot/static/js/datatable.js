// $('#chatbots').DataTable({
//     "lengthChange": false
// });
// $('#chatbots_filter').find('input').attr('placeholder', 'Search Bot...')
// $('#chatbots_filter').find('input').appendTo('#chatbots_filter')
// $('#chatbots_filter').find('label').remove()
$(document).ready(function () {
    var loader = `<i class="fa fa-spin fa-spinner"></i>`
    var csrf_token = $('#csrf-token').val()
    $.ajaxSetup({
        data: { csrfmiddlewaretoken: csrf_token },
    });
    $(document).on('click', '.copy-bot-script', function () {
        var bot_id = $(this).attr('data-bot-id');
        $('#bot-script-modal').modal('show')
        $.ajax({
            url: $.trim($('#get-bot-url').val()),
            type: "POST",
            data: { bot_id: bot_id },
            dataType: 'json',
            success: function (response) {
                if (response.hasOwnProperty('status') &&
                    response.status &&
                    response.hasOwnProperty('data') &&
                    response.data) {
                    var script = `
                    <script>
                    var url = '${location.origin}/static/js/widget.js';
                    var options = {
                        "enabled": true,
                        "chatButtonSetting": {
                            "backgroundColor": "#2B2E50",
                            "ctaText": "",
                            "borderRadius": "25",
                            "marginLeft": "20",
                            "marginBottom": "50",
                            "marginRight": "20",
                            "position": 'right',
                        },
                        "brandSetting": {
                            "brandName": "test",
                            "brandSubTitle": "online",
                            "backgroundColor": "#2B2E50",
                            "ctaText": "Start Chat",
                            "borderRadius": "25",
                            "autoShow": "true",
                            "botChatMsgBackground": "#fff",
                            "userChatMsgBackground": "#2B2E50",
                            "answerButtonBackground": "#2B2E50",
                            "answerButtonTextColor": "#fff",
                            "apiUrl": "${location.origin}/survey-bot/api/bot/master/",
                            "botId": ${response.data.bot.id},
                        }
                    };
                    var s = document.createElement('script');
                    s.type = 'text/javascript';
                    s.async = true;
                    s.src = url;
                    s.onload = function () {
                        CreateSurveyBotWidget(options);
                    };
                    var x = document.getElementsByTagName('script')[0];
                    x.parentNode.insertBefore(s, x);
                    </script>`;
                    script = document.createTextNode(script);
                    $('#bot-script-container').html(script)
                }
            },
            error: function () {
                var title = "Error";
                var message = "Something Went Wrong!"
                var type = true
                var icon = "error"
                display_alert(title, message, type, icon)
            }
        })
    });
    $('.filter-bots').on("keyup", function () {
        var filter = $(this).val().toLowerCase();
        var nodes = document.getElementsByClassName('bot-items');

        for (i = 0; i < nodes.length; i++) {
            if (nodes[i].innerText.toLowerCase().includes(filter)) {
                nodes[i].style.display = "block";
            } else {
                nodes[i].style.display = "none";
            }
        }
    });

    $(document).on('click', '.delete-bot', function () {
        var bot_id = $(this).attr('data-bot-id');
        swal({
            buttons: true,
            title: "Warning",
            text: "Are you sure want to delete this bot",
            icon: 'warning',
            dangerMode: true,
        }).then((value) => {
            if (value) {
                $.ajax({
                    url: $.trim($('#delete-bot-url').val()),
                    type: "POST",
                    data: { bot_id: bot_id },
                    dataType: 'json',
                    success: function (response) {
                        if (response.hasOwnProperty('status') &&
                            response.status &&
                            response.hasOwnProperty('data') &&
                            response.data) {
                            swal({
                                title: "Success",
                                text: response.message,
                                icon: 'success',
                                dangerMode: false,
                            }).then((value) => {
                                reload()
                            })
                        }
                    },
                    error: function () {
                        var title = "Error";
                        var message = "Something Went Wrong!"
                        var type = true
                        var icon = "error"
                        display_alert(title, message, type, icon)
                    }
                })
            } else {
                return false
            }
        })
    })

    $(document).on('click', '.test-bot', function () {
        var bot_id = $(this).attr('data-bot-id')
        var bot_name = $(this).attr('data-bot-name')
        $(this).html(loader)
        preview_chatbot(bot_id, bot_name, $(this));
    });
    function preview_chatbot(chatbotId, bot_name, $button) {
        var url = '/static/js/widget.js?' + Math.floor(Math.random() * 10000000);
        var origin = location.origin;
        var options = {
            "enabled": true,
            "chatButtonSetting": {
                "backgroundColor": "#2B2E50",
                "ctaText": "",
                "borderRadius": "25",
                "marginLeft": "20",
                "marginBottom": "50",
                "marginRight": "20",
                "position": 'right',
            },
            "brandSetting": {
                "brandName": bot_name,
                "brandSubTitle": "online",
                "backgroundColor": "#2B2E50",
                "ctaText": "Start Chat",
                "borderRadius": "25",
                "autoShow": "true",
                "botChatMsgBackground": "#fff",
                "userChatMsgBackground": "#2B2E50",
                "answerButtonBackground": "#2B2E50",
                "answerButtonTextColor": "#fff",
                "apiUrl": origin + "/survey-bot/api/bot/master/",
                "botId": chatbotId,
            }
        };
        if (document.getElementById('phq_chat_widget')) {
            $('#phq_chat_widget').remove()
        }
        var s = document.createElement('script');
        s.type = 'text/javascript';
        s.async = true;
        s.src = url;
        var origin = location.origin;

        s.onload = function () {
            CreateSurveyBotWidget(options);
            $button.html(`<i class="fa-solid fa-circle-play"></i>`)
        };
        var x = document.getElementsByTagName('script')[0];
        //x.parentNode.removeChild(x);
        x.parentNode.insertBefore(s, x);
        //console.log(s)
        (function foo() {
            var b = function moo() {
                var c = document.getElementsByTagName('script');
                c[0].parentElement.removeChild(c[0]);
            }
            var a = setTimeout(b, 1000);
            b = null;
        })();
        foo = null;
    }

    function reload() {
        window.location.reload()
    }

    function display_alert(title, message, type, icon) {
        swal({
            title: title,
            text: message,
            icon: icon,
            dangerMode: type,
        })
    }
});
