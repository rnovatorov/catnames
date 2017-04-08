$(document).ready(function() {
    var url = "http://" + document.domain + ":" + location.port;
    var socket = io.connect(url + "/lobby");

    socket.on("users_in_lobby", function(u) {
        console.log(u);
        var elem = $("#" + u.user_id);
        if (u["in_lobby"] == true) {
            if ( elem[0] ) {
                elem.show();
            } else {
                $("#users_in_lobby_list").append(
                    "<li class='list-group-item' id='" + u.user_id + "'>" +
                        "<img class='avatar img-rounded' src='" + u.avatar + "'/> " +
                        "<a href='" + u.vk_user_page + "'>" +
                            "<span class='full_name'>" + u.full_name + "</span>" +
                        "</a>" +
                    "</li>"
                );
            }
        } else if (u["in_lobby"] == false) {
            elem.hide();
        }
    });

    socket.on("available_rooms", function(r) {
        console.log(r);
        var elem = $("#" + r.room_name);
        if (r["members"].length > 0) {
            if ( elem[0] ) {
                elem.show();
            } else {
                var new_elems = (
                    '<li id=' + r.room_name + ' class="list-group-item">' +
                        '<div class="dropdown">' +
                                '<button class="btn btn-default dropdown-toggle" type="button" data-toggle="dropdown">' +
                                r.room_name +
                                '</button>' +
                            '<ul class="dropdown-menu">'
                );
                if (r["has_quiz_master"]) {
                    new_elems += '<li class="disabled"><a href="/room/' + r.room_name + '/enter/as/quiz-master">Enter as <strong>Quiz-Master</strong></a></li>';
                } else {
                    new_elems += '<li><a href="/room/' + r.room_name + '/enter/as/quiz-master">Enter as <strong>Quiz-Master</strong></a></li>';
                }
                new_elems += (
                        '<li><a href="/room/' + r.room_name + '/enter/as/player">Enter as <strong>Player</strong></a></li>' +
                        '<li><a href="/room/' + r.room_name + '/enter/as/spectator">Enter as <strong>Spectator</strong></a></li>' +
                            '</ul>' +
                        '</div>' +
                    '</li>'
                );
                $("#available_rooms_list").append(new_elems);
            }
        } else if (r["members"].length == 0) {
            elem.hide();
        }
    });
});