function CreateSurveyBotWidget(option = {
    brandSetting: {
        autoShow: true,
        backgroundColor: "#0a6114",
        borderRadius: "25",
        brandImg: "https://res.cloudinary.com/dxxlsebas/image/upload/v1651555411/bot_fxi607.png",
        brandImgData: null,
        brandName: "WATI",
        brandSubTitle: "Typically replies within a day",
        ctaText: "Start Chat",
        welcomeText: "Hi, there! \nHow can I help you?",
        messageText: "",
        botChatMsgBackground:"#ccc",
        userChatMsgBackground:"#000",
        answerButtonBackground:"#334269",
        answerButtonTextColor:"#fff",
        apiUrl:"https://plaintiffhq.com/api/chatbot/master/",
        botId:0,
	    collect:1,
    },
    chatButtonSetting: {
        backgroundColor: "#4dc247",
        borderRadius: "25",
        ctaText: "",
        marginLeft: "0",
        marginRight: "20",
        marginBottom: "20",
        position: "right"
    },
    enabled: false
}) {
    if (option.enabled == false) {
        return;
    }
    if (!option.chatButtonSetting.position) {
        option.chatButtonSetting.position = "right";
        option.chatButtonSetting.marginBottom = "20";
        option.chatButtonSetting.marginLeft = "0";
        option.chatButtonSetting.marginRight = "20";
    }
    var css = document.createElement("STYLE");
    if (window.jQuery) {
        initWidget();
    } else {
        var script = document.createElement("SCRIPT");
        script.src = 'https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js';
        script.type = 'text/javascript';
        script.onload = function () {
            initWidget();
        };
        document.getElementsByTagName("head")[0].appendChild(script);
    }
    function initWidget() {
        if (option.brandSetting.messageText) {
            option.brandSetting.messageText = option.brandSetting.messageText.replaceAll("{{page_link}}", encodeURIComponent(window.location.href));
            option.brandSetting.messageText = option.brandSetting.messageText.replaceAll("{{page_title}}", window.document.title);
            option.brandSetting.messageText = option.brandSetting.messageText.replaceAll("\n", "%0A");
        }
        jQuery('body').append(`<div id="phq_chat_widget">
            <div id="phq-widget-send-button">
                <img src="https://res.cloudinary.com/dxxlsebas/image/upload/v1651555274/chat-icon_amh5k9.svg">
                <div style="color: white; font-size: 18px">${option.chatButtonSetting.ctaText}</div>
            </div>
        </div>`);
        jQuery('#phq_chat_widget').append(`
            <div class='phq-chat-box'>
                <div class='phq-chat-box-header'>
                    <img class='phq-chat-box-brand' onError='this.src="https://res.cloudinary.com/dxxlsebas/image/upload/v1651555411/bot_fxi607.png";' src='${option.brandSetting.brandImg}'/>
                    <div class='phq-chat-box-brand-text'>
                        <div class='phq-chat-box-brand-name'>${option.brandSetting.brandName}</div>
                        <div class='phq-chat-box-brand-subtitle'>${option.brandSetting.brandSubTitle}</div>
                    </div>
                    <div class="phq-chat-bubble-close-btn"><img style="display: table-row" src="https://cdn.shopify.com/s/files/1/0070/3666/5911/files/Vector.png?574"></div>
                </div>

            <main class="phq-chat-box-chat" id="phq-chat-box-chat">
            </main>

            </div>
        `);
        if (option.brandSetting.autoShow) {
            jQuery(".phq-chat-box").css("display", "block");
        } else {
            jQuery(".phq-chat-box").css("display", "none");
        }
        jQuery("#phq_chat_widget").on('click', '.phq-chat-bubble-close-btn', function () {
            jQuery(".phq-chat-box").css("display", "none");
        })
        jQuery("#phq_chat_widget").on('click', '#phq-widget-send-button', function () {
            jQuery(".phq-chat-box").css("display", "block");
        })
        $(document).ready(function(){
        var user_token = uuidv4()
        var loader = `<div class="phq-chat-msg phq-chat-left-msg bot-loader">
                    <img width="50px" src="https://res.cloudinary.com/dxxlsebas/image/upload/v1651555287/dots_oh2peh.gif">
                    </div>`;
        var send_button = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" x="3650" y="3688">
                    <path fill="${option.brandSetting.userChatMsgBackground}" d="M1.1 21.757l22.7-9.73L1.1 2.3l.012 7.912 13.623 1.816-13.623 1.817-.01 7.912z">
                    </path></svg>`

        var hdn_source = $('#hdn_source').val()
        var hdn_code = $('#hdn_code').val()

       	function send_response_to_function(){
            console.log(document.getElementsByClassName('send').length)
            $('.send').click(function(e){
                    var error = validateInputs();
                    if(error == 0){
                        var value= $(this).attr('data-label')
                        html = `<div class="phq-chat-msg phq-chat-right-msg">
                            <div class="phq-chat-msg-bubble">
                                <div class="phq-chat-msg-text">
                                    ${value}
                                </div>
                            </div>
                        </div>`
                        $(this).parent().remove()
                        $('.phq-chat-box-chat').append(html)
                        $(".phq-chat-box-chat").scrollTop($('.phq-chat-box-chat')[0].scrollHeight)
                        load_questions($(this))
                    }
                })
        }
        $(document).on('keyup blur change','.phq-chat-input',function(){
            $(this).next('.send').attr('data-label',$(this).val())
            $(this).next('.send').attr('data-answer',$(this).val())
        })
        load_questions()
        function sleep(time) {
              return new Promise((resolve) => setTimeout(resolve, time));
        }
        function load_questions(evnt=null){
            $element = evnt
            var question_id = 0
            var answer = ''
            data_collection = JSON.stringify({})
            if($element!=null){
                question_id = $element.attr('data-question') || 0
                answer = $element.attr('data-answer') || ''
                if(question_id=='restart'){
                    $('.phq-chat-box-chat').html('')
                }
                var question_code =  $element.attr('data-question-code') || ''
                answer_data = $element.attr('data-label') || ''
                var data_collection = {}
                data_collection[question_code]=answer_data
                data_collection = JSON.stringify(data_collection)
            }

            $.ajax({
                url:option.brandSetting.apiUrl,
                type:'put',
                data:{question_id:question_id,
                answer:answer,
                user_token:user_token,
                botId:option.brandSetting.botId,
                data_collection:data_collection,
                collect:1,
                hdn_code:hdn_code,
                hdn_source:hdn_source,
		        },
                dataType:'json',
                success:function(data){
                    var messageData = data.data
                    messageData = messageData.replaceAll('[[send-button]]',send_button)
                    sleep(500).then(()=>{
                        $('.bot-loader').remove()
                        $('.phq-chat-box-chat').append(messageData)
                        $('.phq-chat-input').trigger('focus')
                        $(".phq-chat-box-chat").scrollTop($('.phq-chat-box-chat')[0].scrollHeight)
                        //this function is called to trigger the send button click
                        send_response_to_function()
		    })
                },
                beforeSend:function(){
                    $('.phq-chat-box-chat').append(loader)
                    $(".phq-chat-box-chat").scrollTop($('.phq-chat-box-chat')[0].scrollHeight)

                }
            })
        }
        $(document).on('keypress','.phq-chat-input',function (e) {
            var key = e.which;
            if(key == 13)  // the enter key code
             {
               $('.send').trigger('click')
               return false;
             }
        });



        function validateInputs(){
            var errorCounter = 0
            input = document.getElementsByClassName("phq-chat-input");
            $(input).each(function(){
                var tag = this.tagName
                var value = $(this).val()
                var msg = ""
                var type = ""
                debugger
                if(tag == 'INPUT'){
                    type = $(this).attr('type')
                    if(type=="text"){
                        if(value == ""){
                            errorCounter++
                            msg = "Please fill this field"
                        }
                    }else if(type == "email"){
                        if(value == ""){
                            errorCounter++
                            msg = "Please fill this field"
                        }else{
                            if(!validateEmail(value)){
                                errorCounter++
                                msg = "Invalid email"
                            }
                        }
                    }else if(type=='phone'){
                        if(value == ""){
                            errorCounter++
                            msg = "Please fill this field"
                        }else{
                            if(!validatePhone(value)){
                                errorCounter++
                                msg = "Invalid Phone Number"
                            }
                        }
                    }else{
                        if(value == ""){
                            errorCounter++
                            msg = "Please fill this field"
                        }
                    }
                }else{
                    if(value == ""){
                        errorCounter++
                        msg = "Please fill this field"
                    }
                }
                $(this).parent().parent().find('.error-msg').html(msg)
                $(this).addClass('field-error')
                $(this).trigger('focus')

            })
            return errorCounter;
        }
        const validateEmail = (email) => {
        return email.match(
            /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
        );
        };
        const validatePhone = (phone) => {
        return phone.match(
            /^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/im
        );
        };
        function uuidv4() {
            return ([1e7]+1e3).replace(/[018]/g, c =>
              (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
            );
        }

    })

    }
    var styles = `
        #phq_chat_widget{
            display: ${option.enabled ? "block" : "none"}
        }
        .phq-chat-bubble-close-btn{
            cursor: pointer;
            position: absolute;
            right: 20px;
            top: 20px;
        }
        .phq-chat-box-brand-text{
            margin-left: 20px;
        }
        .phq-chat-box-brand-name{
            font-size: 16px;
            font-weight: 700;
            line-height: 20px;
        }
        .phq-chat-box-brand-subtitle{
            font-size: 13px;
            line-height: 18px;
            margin-top: 4px;
        }

        .phq-chat-box-header{
            height: 100px;
            max-height: 100px;
            min-height: 100px;
            background:${option.brandSetting.backgroundColor} !important;
            color: white;
            border-radius: 10px 10px 0px 0px;
            display:flex;
            align-items: center;
        }
        .phq-chat-box-brand{
            margin-left: 20px;
            width: 50px;
            height: 50px;
            border-radius: 25px;
            box-shadow: 2px 2px 6px rgba(0,0,0,0.4);
        }
        .phq-chat-box{
            background-color:white;
            z-index: 16000160 !important;
            margin-bottom: 60px;
            width: 480px;
            position: fixed !important;
            bottom: 4% !important;
            ${option.chatButtonSetting.position == "left" ? "left : " + option.chatButtonSetting.marginLeft + "px" : "right : " + option.chatButtonSetting.marginRight + "px"};
            border-radius: 10px;
            box-shadow: 2px 2px 6px rgba(0,0,0,0.4);
            font: 400 normal 15px/1.3 -apple-system, BlinkMacSystemFont, Roboto, Open Sans, Helvetica Neue, sans-serif;
        }
        #phq-widget-send-button {
            margin: 0 0 25px 0 !important;
            padding-left: ${option.chatButtonSetting.ctaText ? "15px" : "0px"};
            padding-right: ${option.chatButtonSetting.ctaText ? "15px" : "0px"};
            position: fixed !important;
            z-index: 16000160 !important;
            bottom: 0 !important;
            text-align: center !important;
            height: 50px;
            min-width: 50px;
            border-radius: ${option.chatButtonSetting.borderRadius}px;
            visibility: visible;
            transition: none !important;
            background-color: ${option.chatButtonSetting.backgroundColor};
            box-shadow: 2px 2px 6px rgba(0,0,0,0.4);
            ${option.chatButtonSetting.position == "left" ? "left : " + option.chatButtonSetting.marginLeft + "px" : "right : " + option.chatButtonSetting.marginRight + "px"};
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content:center;
	    width:50px;
        }
        @media only screen and (max-width: 600px) {
            .phq-chat-box
            {
                width: auto;
                position: fixed !important;
                right: 20px!important;
                left: 20px!important;
            }
        }

        :root {
            --border: 2px solid #ddd;
            --phq-chat-left-msg-bg: ${option.brandSetting.botChatMsgBackground};
            --phq-chat-right-msg-bg: ${option.brandSetting.userChatMsgBackground};
        }
        .phq-chat-box-chat {
            flex: 1;
            overflow-y: auto;
            padding: 10px;
            height:65vh;
            overflow-y:scroll;
        }

        .phq-chat-box-chat::-webkit-scrollbar {
            width: 6px;
        }

        .phq-chat-box-chat::-webkit-scrollbar-track {
            background: #ddd;
        }

        .phq-chat-box-chat::-webkit-scrollbar-thumb {
            background: #bdbdbd;
        }

        .phq-chat-msg {
            display: flex;
            align-items: flex-end;
            margin-bottom: 10px;
        }

        .phq-chat-msg:last-of-type {
            margin: 0;
        }

        .phq-chat-img {
            width: 50px;
            height: 50px;
            margin-right: 10px;
            background: #ddd;
            background-repeat: no-repeat;
            background-position: center;
            background-size: cover;
            border-radius: 50%;
        }

        .phq-chat-msg-bubble {
            max-width: 450px;
            padding: 15px;
            border-radius: 15px;
            background: var(--phq-chat-left-msg-bg);
            box-shadow:0px 0px 2px #999;
        }

        .phq-chat-msg-bubble-button {
            max-width: 100%;
            padding: 15px;

        }

        .phq-chat-info {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }

        .phq-chat-info-name {
            margin-right: 10px;
            font-weight: bold;
        }

        .phq-chat-info-time {
            font-size: 0.85em;
        }

        .phq-chat-left-msg .phq-chat-msg-bubble {
            border-bottom-left-radius: 0;
        }

        .phq-chat-right-msg {
            flex-direction: row-reverse;
        }

        .phq-chat-right-msg .phq-chat-msg-bubble {
            background: var(--phq-chat-right-msg-bg);
            color: #fff;
            border-bottom-right-radius: 0;
        }

        .phq-chat-right-msg .phq-chat-img {
            margin: 0 0 0 10px;
        }
        .phq-btn {
            background-color: ${option.brandSetting.answerButtonBackground};
            border: none;
            color: ${option.brandSetting.answerButtonTextColor};
            padding: 12px 24px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius:7px;
        }
        .field-error{
            border: 1px solid red;
        }
        .control {
            box-sizing: border-box;
            clear: both;
            font-size: 1rem;
            position: relative;
            text-align: inherit;
        }

        .input, .textarea,.phq-chat-input {
            box-shadow: none;
            max-width: 100%;
            width: 100%;
            padding:10px;
            border-radius:5px !important;
            border-width: 2px;
            font-size: 16px;
            height: auto;
            min-height: 46px!important;
            resize: none;
            white-space: pre-wrap;
            word-break: break-word;
            padding-right: 42px;
            border: 1px solid  ${option.brandSetting.userChatMsgBackground} !important;
            color: #666 !important;
        }
        textarea:focus, input:focus{
            outline: none;
        }
        .control.has-icons-left .icon, .control.has-icons-right .icon {
            color: #000;
            height:100%;
            position: absolute;
            top: 0;
            width: 46px;
            z-index: 4;
        }
        .control.has-icons-right .icon.is-right {
            right: 0;
            background: transparent;
            border: 0;
        }
        input[type=number] {
            -moz-appearance: textfield;
        }
        input::-webkit-outer-spin-button,
        input::-webkit-inner-spin-button {
        -webkit-appearance: none;
        margin: 0;
        }
    `

    var styleSheet = document.createElement("style")
    styleSheet.type = "text/css"
    styleSheet.innerText = styles
    document.getElementsByTagName("head")[0].appendChild(styleSheet);
}