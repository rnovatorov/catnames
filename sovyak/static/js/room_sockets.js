var socket;
$(document).ready(function(){
    socket = io.connect("http://" + document.domain + ":" + location.port + "/game");
    socket.on("connect", function() {
        socket.emit("joined", {});
    });
    socket.on("status", function(data) {
        $("#game").val($("#game").val() + "<" + data.msg + ">\n");
        $("#game").scrollTop($("#game")[0].scrollHeight);
    });
    socket.on("message", function(data) {
        $("#game").val($("#game").val() + data.msg + "\n");
        $("#game").scrollTop($("#game")[0].scrollHeight);
    });
    $("#text").keypress(function(e) {
        var code = e.keyCode || e.which;
        if (code == 13) {
            text = $("#text").val();
            $("#text").val("");
            socket.emit("text", {msg: text});
        }
    });
});