var active_count = 4;
var active_idx = 1;
var btn_right_active = 1;
var btn_left_active = 1;

function scroll_load() {
    $(".sscroll-img-list").css("width",
        ($(".sscroll-bar").width() - $(".sbtn-left").outerWidth(true) -
            $(".sbtn-right").outerWidth() - 10 ) + "px");
    var height = ($(".sscroll-bar").width() - $(".sbtn-left").outerWidth(true) -
            $(".sbtn-right").outerWidth() - 7 )/active_count - 7;
    $(".sscroll-img-list").css("height", height + "px");
    $(".sbtn-left").css("height", height + "px");
    $(".sbtn-right").css("height", height + "px");
    $(".sscroll-imgpad").css("height", height + "px");
    $(".sscroll-img").css("max-height", (height-2) + "px");
    $(".sscroll-imgpad").css("width", height + "px");
    $(".sscroll-img").css("max-width", (height-2) + "px");
    $(".sbtn-right").click(move_right);
    $(".sbtn-left").click(move_left);
    display();
    check_btn_display();
}



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
    $(".sscroll-img-list div").removeClass("sscroll-imgpad");
    $(".sscroll-img-list div").removeClass("sscroll-imgpad-inactive");
    for (i=1; i<active_idx; i++)
        $("#default_imgpad_"+i).addClass("sscroll-imgpad-inactive");
    height = $(".sscroll-img-list").height();
    width = $(".sscroll-img-list").width();
    for (i=active_idx; i<=$(".sscroll-img-list").children("div").length; i++) {
        $("#default_imgpad_"+i).addClass("sscroll-imgpad");
        if ($("#default_img_"+i).width() > $("#default_img_"+i).height())
            $("#default_img_"+i).css("margin-top",
                (height-$("#default_img_"+i).height())/2+"px");
    }
}

function check_btn_display() {
    $(".sbtn-right").removeClass("disabled");
    btn_right_active = 1;
    if (active_idx + active_count > $(".sscroll-img-list").children("div").length)
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