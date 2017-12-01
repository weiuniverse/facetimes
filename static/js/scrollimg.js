var active_count = 4;
var active_idx = 1;
var btn_right_active = 1;
var btn_left_active = 1;

$(document).ready(function () {
    $(".sscroll-img-list").css("width",
        ($(".sscroll-bar").innerWidth() - $(".sbtn-left").outerWidth(true) -
            $(".sbtn-right").outerWidth() - 5 ) + "px");
    var height = ($(".sscroll-bar").innerWidth() - $(".sbtn-left").outerWidth(true) -
            $(".sbtn-right").outerWidth() - 5 )/active_count - 7;
    $(".sscroll-img-list").css("height", height + "px");
    $(".sbtn-left").css("height", height + "px");
    $(".sbtn-right").css("height", height + "px");
    $(".sscroll-img").css("height", height + "px");
    $(".sscroll-img").css("width", height + "px");
    $(".sbtn-right").click(move_right);
    $(".sbtn-left").click(move_left);
    check_btn_display();
});



function move_right() {
    if (btn_right_active)
    {
        active_idx += 1;
        display();
        check_btn_display();
    }
}

function move_left() {
    if (btn_left_active)
    {
        active_idx -= 1;
        display();
        check_btn_display();
    }
}

function display() {
    var i = 1;
    $(".sscroll-img-list img").removeClass("sscroll-img");
    $(".sscroll-img-list img").removeClass("sscroll-img-inactive");
    for (i=1; i<active_idx; i++)
        $("#default_img_"+i).addClass("sscroll-img-inactive");
    for (i=active_idx; i<=$(".sscroll-img-list").children("img").length; i++)
        $("#default_img_"+i).addClass("sscroll-img");
}

function check_btn_display() {
    $(".sbtn-right").removeClass("disabled");
    btn_right_active = 1;
    if (active_idx + active_count > $(".sscroll-img-list").children("img").length)
    {
        $(".sbtn-right").addClass("disabled");
        btn_right_active = 0;
    }

    $(".sbtn-left").removeClass("disabled");
    btn_left_active = 1;
    if (active_idx == 1)
    {
        $(".sbtn-left").addClass("disabled");
        btn_left_active = 0;
    }
}