 $(document).ready(function() {

     const socket = io();

     var spectating = "Austria"

     socket.on("add_press", function(msg, cb) {
        if (msg["type"] === "banner"){
            $("#press").append('<div class="banner">'+ msg["text"] +'</div>');
        }
        else{
            let from_to = "From";
            if  (msg["sender"] === spectating){
                from_to = "To";
                msg["sender"] = msg["recipients"][0];
                msg["recipients"] = msg["recipients"].slice(1);
            }

            let cc = "";
            if (msg["recipients"].length > 1) {
                cc = `<div class="cc">
                        <div class="sender-name">cc</div>
                            <div class="sender-flag-container">`
                for (let i=0; i < msg["recipients"].length; i++){
                    if (msg["recipients"][i] !== spectating){ cc.append(`<img src="/static/flags/${msg["recipients"][i]}.svg" class="press-flag">`)}
                }
                cc.append("</div></div>")
            }

            let head = `
                    <div class="message-head">
                        <div class="sender-info">
                            <div class="sender-name">${from_to} ${msg["sender"]}</div>
                            <div class="sender-flag-container">
                                <img src="/static/flags/${msg["sender"]}.svg" class="press-flag">
                            </div>
                        </div>
                        ${cc}
                    </div>`
            let body = `<span class="message-body">${msg["body"]}</span>`

            let message = ""
            if (from_to === "From"){
                message = `<div class="message">${head} ${body}</div>`
            }
            else{
                message = `<div class="message">${body} ${head}</div>`
            }

            $("#press").append(message)
        }
    });

    socket.on("update_screen", function(msg, cb) {
        if (msg["screen"] === "off"){
            $(".screen-image").hide();
        }
        else{
           $("#flag").attr("src","/static/flags/" + msg["country_image"]);
           $("#model").attr("src","/static/logos/" + msg["model_image"]);
           $(".screen-image").show();
        }
    });
    socket.on("refresh_map", function(msg, cb) {
        console.log("e")
        $("#map").attr("src","/static/map.png?uid=" + new Date().getTime())
    });
});