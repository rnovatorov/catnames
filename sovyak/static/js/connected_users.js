$(document).ready(function() {
    var url = "http://" + document.domain + ":" + location.port;
    var socket = io.connect(url + "/lobby");

    socket.on("connected_users", function(u) {
        console.log(u);
        if (u["online"] == true) {
            var elem = $("#" + u.user_id);
            if ( elem[0] ) {
                elem.show();
            } else {
                $("#users_online_list").append(
                    "<li id='" + u.user_id + "'>" +
                        "<img class='avatar' src='" + u.avatar + "'/> " +
                        "<a href='" + u.vk_user_page + "'>" +
                            "<span class='full_name'>" + u.full_name + "</span>" +
                        "</a>" +
                    "</li>"
                );
            }
        } else if (u["online"] == false) {
            var elem = $("#" + u.user_id);
            elem.hide();
        }
    });
});