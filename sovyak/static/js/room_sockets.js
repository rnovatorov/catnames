$(document).ready(function(){
    var url = "http://" + document.domain + ":" + location.port + "/game";
    var socket = io.connect(url);

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

    $(".nav a").click(function() {
        socket.emit("left", {}, function() {
            socket.disconnect();
        });
    });
});
