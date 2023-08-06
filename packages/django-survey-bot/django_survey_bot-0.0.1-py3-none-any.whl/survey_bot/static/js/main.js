$(document).ready(function () {
    var question_mapping = {}
    var connections = []
    var jsplumb_connections = {}
    var jsplumb_postions = {}
    var question_type_id = 0
    var question_order_data = ""
    var jsplumb_connections_data = ""
    var jsplumb_connections_data = ""
    var loader = `<i class="fa fa-spin fa-spinner"></i>`
    var question_type_obj = $('#question-type-dict').val()
    question_type_obj = JSON.parse(question_type_obj)
    var jsplumb_connections_obj = $('#jsplumb-connections-dict').val()
    jsplumb_connections_obj = JSON.parse(jsplumb_connections_obj)

    var non_option_fields = [];//the field types not contains options
    $.each(question_type_obj, function (key, value) {
        if (value.is_option == 0) {
            non_option_fields.push(key)
        }
    })
    //console.log(Object.keys(jsplumb_connections_obj).length)
    console.log(non_option_fields)
    var questionOptionsObj = {};//to save all the options in an object
    CKEDITOR.replace('question');
    CKEDITOR.config.height = "100px"
    var ckeditor = CKEDITOR.instances["question"]
    var csrf_token = $('#csrf-token').val()
    $.ajaxSetup({
        data: { csrfmiddlewaretoken: csrf_token },
    });
    $("#bot-menu-toggle").click(function (e) {
        e.preventDefault();
        var isIE11 = !!navigator.userAgent.match(/Trident.*rv\:11\./);
        $("#bot-button-toggle").toggleClass("fa-solid fa-arrow-left fa-solid fa-arrow-right")
        $("#wrapper").toggleClass("toggled");
        if ($("#wrapper").hasClass("toggled")) {
            $('#bot-sidebar').hide()
        } else {
            $('#bot-sidebar').show()
        }

    });
    $(document).on('click', '.question-type', function () {
        var question_type = $(this).attr('data-field-type')
        var question_heading = question_type_obj[question_type].label
        var question_icon = question_type_obj[question_type].icon
        var question_icon_tag = $('#question-icon').attr("data-src")
        var default_question = question_type_obj[question_type].default_question
        $('#question-conf-container').show()
        $('#bot-nav-menus').hide()
        $('#question-heading').html(question_heading)
        $('#question-icon').attr('src', question_icon_tag + question_icon)
        ckeditor.setData(default_question)
        if (question_type == 1) {
            $('#button-options-container').show()
        } else {
            $('#button-options-container').hide()
        }
        question_type_id = question_type
    })
    $('.close-question-container').click(function () {
        $('#question-conf-container').hide()
        $('#bot-nav-menus').show()
        $('#save-question').hide();
        $('#create-question').show();
        var options = `
            <tr>
                <th><input type="text" placeholder="Label *" name="button_option_label" class="form-control button_option_label required" autocomplete="off"></th>
                <th><button type="button" class="btn btn-secondary btn-delete-q-option"><i class="fa fa-trash"></i></button></th>
            </tr>
        `
        $('#button-options').html(options)

    })
    $("#add-row").click('click', function () {
        var $tr = $("#button-options tr:last").clone();
        $tr.find('input').val('');
        $("#button-options").append($tr);
    });
    $(document).on('click', '.btn-delete-q-option', function () {
        var tr = $("#button-options tr").length
        if (tr > 1) {
            $(this).closest('tr').remove();
        } else {
            alert("you cannot remove all rows")
        }
    })
    function validate() {
        var error = 0
        if (question_type_id == 1) {
            $('.required').each(function () {
                if ($(this).val() == "") {
                    $(this).addClass("is-invalid")
                    error++;
                } else {
                    $(this).removeClass("is-invalid")
                }
            });
        }
        if ((ckeditor.getData() == "") || (ckeditor.getData() == " ")) {
            $('#cke_question').addClass("is-invalid-imp")
            error++;
        } else {
            $('#cke_question').removeClass("is-invalid-imp")
        }
        return error
    }
    $('#create-question').click(function (e) {
        e.preventDefault();
        var error = validate()
        if (error == 0) {
            add_or_save_question()
        } else {
            var title = "Error";
            var message = "Please fill all the mandatory fields"
            var type = true
            var icon = "error"
            display_alert(title, message, type, icon)
        }
    })
    function display_alert(title, message, type, icon) {
        swal({
            title: title,
            text: message,
            icon: icon,
            dangerMode: type,
        })
    }
    $(document).on('click', '.question-read-more', function () {
        var dots = $(this).parent().find('.question-dots')
        var moreText = $(this).parent().find('.question-more')
        if (dots.css('display') == 'none') {
            dots.css('display', 'inline');
            $(this).html("Read more");
            moreText.hide()
        } else {
            dots.hide()
            $(this).html("Read less");
            moreText.css('display', 'inline');
        }
    })
    get_all_chatbot_questions()
    function get_all_chatbot_questions() {
        var bot_id = $('#survey-bot-id').val()
        $.ajax({
            url: $.trim($('#get-all-bot-questions-url').val()),
            type: "POST",
            data: { bot_id: bot_id },
            dataType: 'json',
            success: function (response) {
                if (response.hasOwnProperty('status') &&
                    response.status &&
                    response.hasOwnProperty('data') &&
                    response.data) {
                    $('#canvas').html(response.data.posts_html)
                    load_jsplumb_flowchart()
                }
            }
        })
    }

    function add_or_save_question(question_id=0) {
        var bot_id = $('#survey-bot-id').val()
        isError = false
        questionData = ckeditor.getData()//$("#question").val()
        fieldID = question_type_id;
        let optionsArr = []
        if ($('.button_option_label').length > 0) {
            for (var i = 0; i < $('.button_option_label').length; i++) {
                if (non_option_fields.indexOf(fieldID) == -1) {
                    optionsArr.push({
                        label: document.getElementsByClassName('button_option_label')[i].value,
                        value: document.getElementsByClassName('button_option_label')[i].value,
                    })
                }
            }
        }
        questionOptionsObj[question_id] = optionsArr
        currentDataObject = {}
        currentDataObject.chatbot_id = bot_id
        currentDataObject.question_id = question_id
        currentDataObject.question = questionData
        currentDataObject.field_type = fieldID
        currentDataObject.options = optionsArr
        $.ajax({
            url: $.trim($('#save-bot-question-url').val()),
            type: "POST",
            data: { questionData: JSON.stringify(currentDataObject) },
            dataType: 'json',
            success: function (response) {
                if (response.hasOwnProperty('status') &&
                    response.status &&
                    response.hasOwnProperty('data') &&
                    response.data) {
                    publish_survey_bot()
                }
            }
        })
    }
    $('#publish-bot').click(function () {
        publish_survey_bot(1)
    })
    $(document).on('click', '.edit-bot-question', function () {
        $('#save-question').show();
        $('#create-question').hide();
        var bot_id = $('#survey-bot-id').val()
        var question_id = $(this).attr('data-id')
        var question_type = $(this).attr('data-question-type')
        $('#save-question').attr('data-question-id',question_id)
        $.ajax({
            url: $.trim($('#get-question-details-url').val()),
            type: "POST",
            data: {bot_id:bot_id,question_id:question_id},
            dataType: 'json',
            success: function (response) {
                if (response.hasOwnProperty('status') &&
                    response.status &&
                    response.hasOwnProperty('data') &&
                    response.data) {
                    ckeditor.setData(response.data.question)
                    if(response.data.options.length > 0){
                        let rows = ""
                        let options = response.data.options
                        for(i=0;i<options.length;i++){
                            rows+=`
                                <tr>
									<th><input type="text" value="${options[i]}" placeholder="Label *" name="button_option_label" class="form-control button_option_label required" autocomplete="off"></th>
									<th><button type="button" class="btn btn-secondary btn-delete-q-option"><i class="fa fa-trash"></i></button></th>
								</tr>
                            `
                        }
                        $('#button-options').html(rows)
                    }
                    $(`[data-field-type="${question_type}"]`).trigger('click')
                }
            }
        })
    })
    $('#save-question').click(function(){
        var question_id = $(this).attr('data-question-id')
        add_or_save_question(question_id)
    })
    $(document).on('click', '.delete-bot-question', function () {
        var bot_id = $('#survey-bot-id').val()
        var question_id = $(this).attr('data-id')
        swal({
            buttons: true,
            title: "Warning",
            text: "Are you sure want to delete this question",
            icon: 'warning',
            dangerMode: true,
        }).then((value) => {
            if (value) {
                $.ajax({
                    url: $.trim($('#delete-bot-question-url').val()),
                    type: "POST",
                    data: { question_id: question_id, bot_id: bot_id },
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
    function publish_survey_bot(publish = 0) {
        var bot_id = $('#survey-bot-id').val()
        var bot_name = $('#survey-bot-name').text()
        var data = {
            bot_id: bot_id,
            is_publish: publish,
            bot_name: bot_name,
        }
        if (Object.keys(question_mapping).length > 0) {
            send_request = true;
            question_order_data = JSON.stringify(question_mapping)
            data['questionOrderData'] = question_order_data
        }
        if (Object.keys(jsplumb_connections).length > 0) {
            send_request = true;
            jsplumb_connections_data = JSON.stringify(jsplumb_connections)
            data['jsplumbConnectionData'] = jsplumb_connections_data
        }
        jsplumb_flowchart_positions()
        if (Object.keys(jsplumb_postions).length > 0) {
            send_request = true;
            jsplumb_position_data = JSON.stringify(jsplumb_postions)
            data['jsplumbPositionsData'] = jsplumb_position_data
        }
        $.ajax({
            url: $.trim($('#publish-bot-url').val()),
            type: "POST",
            data: data,
            dataType: 'json',
            success: function (response) {
                if (response.hasOwnProperty('status') &&
                    response.status &&
                    response.hasOwnProperty('data') &&
                    response.data) {
                    if (publish == 1) {
                        swal({
                            title: "Success",
                            text: response.message,
                            icon: 'success',
                            dangerMode: false,
                        })
                    } else {
                        reload()
                    }
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
    }
    function jsplumb_flowchart_positions() {
        var ele = document.getElementsByClassName('window')
        $(ele).each(function () {
            var quesiton_box_id = $(this).attr('id')
            jsplumb_postions[quesiton_box_id] = $(this).attr('style') || ""
        })
    }
    function load_jsplumb_flowchart() {
        (function () {

            var listDiv = document.getElementById("list"),
                updateConnections = function (conn, remove) {
                    if (!remove) connections.push(conn);
                    else {
                        var idx = -1;
                        for (var i = 0; i < connections.length; i++) {
                            if (connections[i] === conn) {
                                idx = i;
                                break;
                            }
                        }
                        if (idx !== -1) connections.splice(idx, 1);
                    }
                    question_mapping = {}
                    jsplumb_connections = {}

                    if (connections.length > 0) {
                        for (var j = 0; j < connections.length; j++) {
                            s = connections[j].sourceId + "-" + connections[j].targetId;
                            var source = connections[j].sourceId
                            var target = connections[j].targetId
                            jsplumb_connections[source] = target
                            source = source.split("_")
                            var mapping = {}
                            var next_question = target
                            var source_question = source[0]

                            if (source.length > 1) {
                                mapping[source[1]] = target
                            }
                            mapping['default'] = target

                            if (question_mapping[source_question] != undefined) {
                                default_question = Object.keys(question_mapping[source_question][0])[0]
                                default_question = question_mapping[source_question][0][default_question]
                                mapping['default'] = default_question
                                question_mapping[source_question].push(mapping)
                            } else {
                                question_mapping[source_question] = [mapping]
                            }


                        }
                    }

                };

            jsPlumbBrowserUI.ready(function () {
                var instance = window.j = jsPlumbBrowserUI.newInstance({
                    dragOptions: { cursor: 'pointer', zIndex: 2000 },
                    paintStyle: { stroke: '#666' },
                    endpointHoverStyle: { fill: "orange" },
                    hoverPaintStyle: { stroke: "orange" },
                    endpointStyle: { width: 20, height: 16, stroke: '#666' },
                    endpoint: "Blank",
                    anchors: ["TopCenter", "TopCenter"],
                    container: canvas,
                    dropOptions: { activeClass: "dragActive", hoverClass: "dropHover", tolerance: "touch" },
                    connectionOverlays: [{
                        type: "Arrow",
                        options: {
                            location: 1,
                            visible: false,
                            width: 15,
                            length: 15,
                            id: "ARROW",
                            events: {
                                click: function click() {
                                    //alert("you clicked on the arrow overlay");
                                }
                            }
                        }
                    }],
                });

                // suspend drawing and initialise.
                //instance.setContainer($("body"));
                instance.batch(function () {
                    // bind to connection/connectionDetached events, and update the list of connections on screen.
                    instance.bind("connection", function (info, originalEvent) {
                        updateConnections(info.connection);
                    });
                    instance.bind("connection:detach", function (info, originalEvent) {
                        updateConnections(info.connection, true);
                        // alert()
                    });

                    instance.bind("connection:move", function (info, originalEvent) {
                        //  only remove here, because a 'connection' event is also fired.
                        // in a future release of jsplumb this extra connection event will not
                        // be fired.
                        updateConnections(info.connection, true);
                    });

                    instance.bind("click", function (component, originalEvent) {
                        alert("click!")
                    });

                    // configure some drop options for use by all endpoints.
                    var exampleDropOptions = {
                        tolerance: "touch",
                        hoverClass: "dropHover",
                        activeClass: "dragActive"
                    };

                    var color2 = "#67B22C";
                    var exampleEndpointSource = {
                        endpoint: { type: "Dot", options: { radius: 9} },
                        anchor: "Right",
                        paintStyle: { fill: color2 },
                        source: true,
                        scope: "blue",
                        connectorStyle: { stroke: color2, strokeWidth: 4 },
                        connector: { type: "Flowchart", options: { stub: [20, 40], gap: 10, cornerRadius: 5, alwaysRespectStubs: true } },
                        maxConnections: 1,
                        target: false,
                        dropOptions: exampleDropOptions,
                    };
                    var color2 = "#999";
                    var exampleEndpointTarget = {
                        endpoint: { type: "Rectangle", options: { radius: 6, width: 10 } },
                        anchor: ["Top","Bottom","Left"],
                        paintStyle: { fill: color2 },
                        source: false,
                        scope: "blue",
                        connectorStyle: { stroke: color2, strokeWidth: 4 },
                        connector: { type: "Flowchart", options: { stub: [20, 40], gap: 10, cornerRadius: 5, alwaysRespectStubs: true ,hoverClass:"fooHover"} },
                        maxConnections: 100,
                        target: true,
                        dropOptions: exampleDropOptions,
                    };

                    var plumb_connector = document.getElementsByClassName('plumb-connector')

                    $(plumb_connector).each(function () {
                        var is_option = $(this).attr('data-option');
                        var is_no_option = $(this).attr('data-no-option');
                        uuid1 = $(this).attr('id')
                        var count = $('#' + uuid1 + ' .option').length
                        //console.log(count)
                        if (is_option == 1) {
                            uuid1 = uuid1 + "_1"
                            instance.addEndpoint(this, { uuid: uuid1 }, exampleEndpointSource);
                            //console.log(uuid1)
                        } else if (is_no_option == 0) {
                            uuid2 = uuid1 + "_1"
                            uuid3 = uuid1 + "_2"
                            instance.addEndpoint(this, { uuid: uuid2 }, exampleEndpointSource);
                            instance.addEndpoint(this, { uuid: uuid3 }, exampleEndpointTarget);
                        }
                        else {
                            uuid1 = uuid1 + "_2"
                            //console.log(uuid1)
                            instance.addEndpoint(this, { uuid: uuid1 }, exampleEndpointTarget);

                        }
                    })

                    $.each(jsplumb_connections_obj, function (source, target) {
                        //console.log('{{x.source}}_{{x.target}}_'+is_option.length)
                        instance.connect({ uuids: [source + '_1', target + '_2'] });
                    })

                    var hideLinks = document.querySelectorAll(".drag-drop-demo .hide");
                    instance.on(hideLinks, "click", function (e) {
                        instance.toggleVisible(this.parentNode);
                        instance.consume(e);
                    });

                    var dragLinks = document.querySelectorAll(".drag-drop-demo .drag");
                    instance.on(dragLinks, "click", function (e) {
                        var s = instance.toggleDraggable(this.parentNode);
                        this.innerHTML = (s ? 'disable dragging' : 'enable dragging');
                        instance.consume(e);
                    });

                    var detachLinks = document.querySelectorAll(".drag-drop-demo .detach");
                    instance.on(detachLinks, "click", function (e) {
                        instance.deleteConnectionsForElement(this.parentNode);
                        instance.consume(e);
                    });


                });
                instance.repaintEverything()
            });
        })();
    }

    // preview bot
    $(document).on('click', '#bot-preview-btn', function(e){
        var bot_id = $('#survey-bot-id').val()
        var bot_name = $('#survey-bot-name').text()
        $(this).html(loader)
        preview_chatbot(bot_id,bot_name,$(this))
    })
    function preview_chatbot(chatbotId,bot_name,$button) {
        var url = '/static/js/widget.js?'+ Math.floor(Math.random()* 10000000);
        var origin = location.origin;
        var options = {
            "enabled": true,
            "chatButtonSetting": {
                "backgroundColor": "#47456B",
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
                "apiUrl": origin+"/survey-bot/api/bot/master/",
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
            $button.html(`<i class="la la-globe"></i> <span data-v-gettext>Preview</span>`)
        };
        var x = document.getElementsByTagName('script')[0];
        //x.parentNode.removeChild(x);
        x.parentNode.insertBefore(s, x);
        //console.log(s)
        (function foo(){
            var b=function moo(){
                var c=document.getElementsByTagName('script');
                c[0].parentElement.removeChild(c[0]);
            }
            var a=setTimeout(b,1000);
            b=null;
        })();
        foo=null;
    }
    
    function reload() {
        window.location.reload()
    }
});