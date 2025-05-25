 $(document).ready(function() {

    var socket = io();

    socket.on("add_press", function(msg, cb) {
        if (msg["type"] == "banner"){
            $("#press").append('<div class="banner">'+ msg["text"] +'</div>');
        }
        else{
            $("#press").append('<div class="message"><span class="message-head"><span class="sender"><span>From:</span>'+'<img class="press-flag" src="/static/flags/' + msg["sender"] + '.svg"><span>'+msg["sender"]+'</span>'+'</span> <span class="recipient"> To:')
            for(let i=0; i < msg["recipients"].length; i++){
                $("#press .message:last-child .recipient").append('<img class="press-flag" src="/static/flags/' + msg["recipients"][i] + '.svg"/><span>'+msg["recipients"][i]+'</span>')
            }
            $("#press .message:last-child").append('<span class="message-body"> ' + msg["body"] + '</span>')

        }
    });

    socket.on("update_screen", function(msg, cb) {
        if (msg["screen"] == "off"){
            $(".screen-image").hide();
        }
        else{
           $("#flag").attr("src","/static/flags/" + msg["country_image"]);
           $("#model").attr("src","/static/logos/" + msg["model_image"]);
           $(".screen-image").show();
        }
    });
});