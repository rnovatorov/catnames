$(document).ready(function(){
    var url = "http://" + document.domain + ":" + location.port + "/game";
    var socket = io.connect(url);

    socket.on("connect", function() {
        socket.emit("joined", {});
    });

    socket.on("status", function(data) {
        $("#game").val($("#game").val() + "<" + data.msg + ">\n");
        $("#game").scrollTop($("#game")[0].scrollHeight);

        console.log(data);

        var elem = $("#user_" + data.u.user_id);

        elem.remove();

        if (data.action == "connected") {
            var new_elem =
                "<li class='list-group-item' id='user_" + data.u.user_id + "'>" +
                    "<img class='avatar img-rounded' src='" + data.u.avatar + "'/> " +
                    "<a href='" + data.u.vk_user_page + "'>" +
                        "<span class='full_name'>" + data.u.full_name + "</span>" +
                    "</a>";
            if (data.u.role == "quiz-master") {
                new_elem +=
                    "<span class='glyphicon glyphicon-star'></span>";
            } else if (data.u.role == "player") {
                new_elem +=
                    "<span class='glyphicon glyphicon-user'></span>" +
                    "<span class='score badge'>" + data.u.score + "</span>";
            } else if (data.u.role == "spectator") {
                new_elem +=
                    "<span class='glyphicon glyphicon-eye-open'></span>";
            }
            new_elem +=
                "</li>";
            $("#users_in_room_list").append(new_elem);
        }
    });

    socket.on("message", function(data) {
        $("#game").val($("#game").val() + data.msg + "\n");
        $("#game").scrollTop($("#game")[0].scrollHeight);
    });

    $("#user_input").keypress(function(e) {
        var code = e.keyCode || e.which;
        if (code == 13) {
            text = $("#user_input").val();
            if (text != "") {
                $("#user_input").val("");
                socket.emit("user_input", {msg: text});
            }
        }
    });
});
