var active_count = 4;
var active_idx = [];
var btn_right_active = [];
var btn_left_active = [];
var id_list = [];
var rand_idx = 1;

function scroll_load() {
    setup();
    for (var i = 0; i < id_list.length; i++) {
        id = id_list[i];
        active_idx[i] = 1;
        btn_left_active[i] = 1;
        btn_right_active[i] = 1;
        init_bar(id);
    }
}

function setup() {
    obj = $(".sscroll-bar");
    for (var i = 0; i < obj.length; i++) {
        if (obj[i].id === null || obj[i].id === undefined || obj[i].id === '') {
            obj[i].id = random_id();
        }
        id_list.push('#' + obj[i].id);
    }
}

function init_bar(id) {
    console.log($(id).width() + " " + $(id + " .sbtn-left").outerWidth(true) + " " +
        $(id + " .sbtn-right").outerWidth(true));
    $(id + " .sscroll-img-list").css("width",
        ($(id).width() - $(id + " .sbtn-left").outerWidth(true) -
            $(id + " .sbtn-right").outerWidth(true) - 10 ) + "px");
    var height = ($(id).width() - $(id + " .sbtn-left").outerWidth(true) -
        $(id + " .sbtn-right").outerWidth(true) - 10 ) / active_count - 6;
    $(id).css("height", (height+4) + "px");
    $(id + " .sscroll-img-list").css("height", (height+2) + "px");
    $(id + " .sbtn-left").css("height", (height+2) + "px");
    $(id + " .sbtn-right").css("height", (height+2) + "px");
    $(id + " .sscroll-img-list div").css("height", (height) + "px");
    $(id + " .sscroll-img-list div img").css("max-height", (height - 6) + "px");
    $(id + " .sscroll-img-list div").css("width", (height) + "px");
    $(id + " .sscroll-img-list div img").css("max-width", (height - 6) + "px");

    $(id + " .sbtn-right").unbind('click');
    $(id + " .sbtn-left").unbind('click');
    $(id + " .sbtn-right").click(move_right);
    $(id + " .sbtn-left").click(move_left);
    display(id);
    check_btn_display(id);
}

function random_id() {
    while ($('#scroll_bar_' + rand_idx)[0])
        rand_idx++;
    return 'scroll_bar_' + rand_idx;
}

function move_right() {
    id = '#' + $(this)[0].parentNode.id;
    idx = getidxbyid(id);
    if (btn_right_active[idx]) {
        active_idx[idx] += 1;
        display(id);
        check_btn_display(id);
    }
}

function move_left() {
    id = '#' + $(this)[0].parentNode.id;
    idx = getidxbyid(id);
    if (btn_left_active[idx]) {
        active_idx[idx] -= 1;
        display(id);
        check_btn_display(id);
    }
}

function display(id) {
    var i = 1;
    $(id + " .sscroll-img-list div").removeClass("sscroll-imgpad");
    $(id + " .sscroll-img-list div").removeClass("sscroll-imgpad-inactive");
    $(id + " .sscroll-img-list div").removeClass("sscroll-imgpad-active");
    $(id + " .sscroll-img-list div").removeClass("sscroll-imgpad-halfactive");
    idx = getidxbyid(id);
    for (i = 1; i < active_idx[idx]; i++)
        $(id + " .sscroll-img-list div:eq(" + (i - 1) + ")").addClass("sscroll-imgpad-inactive");
    height = $(id + " .sscroll-img-list").height();
    width = $(id + " .sscroll-img-list").width();

    for (i = active_idx[idx]; i <= $(id + " .sscroll-img-list div").length; i++) {
        ele = $(id + " img:eq(" + (i - 1) + ")");
        $(id + " .sscroll-img-list div:eq(" + (i - 1) + ")").addClass("sscroll-imgpad sscroll-imgpad-halfactive");
        console.log((i - 1) + " " + ele.width() + " " + ele.height() +" "+width+" "+height);
        ew = ele.width();
        eh = ele.height();
        console.log(ew, eh, width, height);
        if (ew > eh) {
            ele.css("width", (height-6) + "px");
            ele.css("height", "auto");
            ele.css("margin-top", (height - eh*height/ew) / 2 + "px");
        }
        else {
            ele.css("height", (height-6)+"px", "width", "auto", "margin-top", 0);

        }
    }
    if (focus[idx] >= 0) {
        $(id + ">div>div:eq(" + (focus[idx]) + ")").addClass("sscroll-imgpad-active");
        $(id + ">div>div:eq(" + (focus[idx]) + ")").removeClass("sscroll-imgpad-halfactive");
    }

}

function check_btn_display(id) {
    idx = getidxbyid(id);
    $(id + " .sbtn-right").removeClass("disabled");
    btn_right_active[idx] = 1;
    if (active_idx[idx] + active_count > $(id + " .sscroll-img-list div").length) {
        $(id + " .sbtn-right").addClass("disabled");
        btn_right_active[idx] = 0;
    }

    $(id + " .sbtn-left").removeClass("disabled");
    btn_left_active[idx] = 1;
    if (active_idx[idx] === 1) {
        $(id + " .sbtn-left").addClass("disabled");
        btn_left_active[idx] = 0;
    }
}

function getidxbyid(id) {
    for (var i = 0; i < id_list.length; i++)
        if (id_list[i] === id)
            return i;
    return -1;
}
