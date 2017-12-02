var augment_img_id = undefined;

function load() {
    $("#image_canvas").css("width",
        document.getElementById("image").offsetWidth - 30);// 30 is margin-left + margin_right
    $("#image_canvas").css("height",
        document.getElementById("image_canvas").offsetWidth);
    $(".sscroll-img-list div").click(upload_default);
    $('#file').change(function () {
        upload();
    });
    $(".aug_btn").click(augment);
    canvas_load();
    scroll_load();
}

function upload() {
    var form = new FormData();
    form.append("file", $('#file')[0].files[0]);
    form.append("name", "jdlsajdlkas");
    form.append("order", "1");

    var settings = {
        "async": true,
        "crossDomain": true,
        "url": "/upload/",
        "method": "POST",
        "processData": false,
        "contentType": false,
        "mimeType": "multipart/form-data",
        "data": form
    };

    $.ajax(settings).done(function (response) {
        $("#response_json p").text(response);
        //console.log("response=" + response);
        response_obj = JSON.parse(response);
        if (response_obj["rs"] === "Success") {
            var img = new Image();
            img.src = response_obj["info"];
            img.onload = function () {
                default_canvas(img);
                $("#face_image_list1").empty();
                $("#face_image_list2").empty();
                if (response_obj["faces_list"].length == 0) {
                    alert("No face found.");
                }
                height = $("#face_image_list1").height();
                width = $("#face_image_list1").width();
                height2 = $("#face_image_list2").height();
                width2 = $("#face_image_list2").width();

                for (i = 1; i <= response_obj["faces_list"].length; i++) {
                    face_obj = response_obj["faces_list"][i - 1];
                    console.log(face_obj);
                    draw_face(face_obj['pt_x'], face_obj['pt_y'], face_obj['width'], face_obj['height']);
                    // Set properties of #face_image_list1
                    $("#face_image_list1").append(
                        '<div class="sscroll-imgpad" id="face_imgpad_' + i + '">' +
                        '<img class="sscroll-img" id="face_image_' + i +
                        '" src="' + face_obj['base64'] + '" alt="Faces"></div>');
                    $("#face_image_" + i).css("max-height", $("#face_image_list1").height() + "px");
                    $("#face_imgpad_" + i).css("height", $("#face_image_list1").height() + "px");
                    $("#face_image_" + i).css("max-width", $("#face_image_list1").height() + "px");
                    $("#face_imgpad_" + i).css("width", $("#face_image_list1").height() + "px");
                    if ($("#face_image_" + i).width() > $("#face_image_" + i).height()) {
                        $("#face_image_" + i).css("margin-top",
                            (height - $("#face_image_" + i).height()) / 2 + "px");
                        $("#face_image_" + i).css("width", width);
                    } else {
                        $("#face_image_" + i).css("height", height);
                    }
                    $("#face_image_" + i).click(get_landmark);

                    // Set properties of #face_image_list2
                    $("#face_image_list2").append(
                        '<div class="sscroll-imgpad" id="face_imgpad2_' + i + '">' +
                        '<img class="sscroll-img" id="face_image2_' + i +
                        '" src="' + face_obj['base64'] + '" alt="Faces"></div>');
                    $("#face_image2_" + i).css("max-height", height2 + "px");
                    $("#face_imgpad2_" + i).css("height", height2 + "px");
                    $("#face_image2_" + i).css("max-width", height2 + "px");
                    $("#face_imgpad2_" + i).css("width", height2 + "px");
                    if ($("#face_image2_" + i).width() > $("#face_image2_" + i).height()) {
                        $("#face_image2_" + i).css("margin-top",
                            (height2 - $("#face_image2_" + i).height()) / 2 + "px");
                        $("#face_image2_" + i).css("width", width2);
                    } else {
                        $("#face_image2_" + i).css("height", height2);
                    }
                    $("#face_image2_" + i).click(function () {
                        augment_img_id = '#' + $(this).attr("id");
                        console.log('click ' + augment_img_id);
                    });

                }

            };

        } else {
            alert(response_obj["info"]);
        }
    });
}

function upload_default() {
    var src = $(this).children("img").attr("src");
    var i = 1;
    console.log($(this));
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        url: "/upload_default/",
        complete: function (XMLHttpRequest, textStatus) {
            // alert(XMLHttpRequest.responseText + "\n" + textStatus);
            if (XMLHttpRequest.status === 200) { // Success
                $("#response_json p").text(XMLHttpRequest.responseText);
                response_obj = JSON.parse(XMLHttpRequest.responseText);
                if (response_obj["rs"] === "Success") {
                    var img = new Image();
                    img.src = response_obj["info"];
                    img.onload = function () {
                        default_canvas(img);
                        $("#face_image_list1").empty();
                        $("#face_image_list2").empty();
                        if (response_obj["faces_list"].length == 0) {
                            alert("No face found.");
                        }

                        height = $("#face_image_list1").height();
                        width = $("#face_image_list1").width();
                        height2 = $("#face_image_list2").height();
                        width2 = $("#face_image_list2").width();

                        for (i = 1; i <= response_obj["faces_list"].length; i++) {
                            face_obj = response_obj["faces_list"][i - 1];
                            console.log(face_obj);
                            draw_face(face_obj['pt_x'], face_obj['pt_y'], face_obj['width'], face_obj['height']);
                            // Set properties of #face_image_list1
                            $("#face_image_list1").append(
                                '<div class="sscroll-imgpad" id="face_imgpad_' + i + '">' +
                                '<img class="sscroll-img" id="face_image_' + i +
                                '" src="' + face_obj['base64'] + '" alt="Faces"></div>');
                            $("#face_image_" + i).css("max-height", $("#face_image_list1").height() + "px");
                            $("#face_imgpad_" + i).css("height", $("#face_image_list1").height() + "px");
                            $("#face_image_" + i).css("max-width", $("#face_image_list1").height() + "px");
                            $("#face_imgpad_" + i).css("width", $("#face_image_list1").height() + "px");
                            if ($("#face_image_" + i).width() > $("#face_image_" + i).height()) {
                                $("#face_image_" + i).css("margin-top",
                                    (height - $("#face_image_" + i).height()) / 2 + "px");
                                $("#face_image_" + i).css("width", width);
                            } else {
                                $("#face_image_" + i).css("height", height);
                            }
                            $("#face_image_" + i).click(get_landmark);

                            // Set properties of #face_image_list2
                            $("#face_image_list2").append(
                                '<div class="sscroll-imgpad" id="face_imgpad2_' + i + '">' +
                                '<img class="sscroll-img" id="face_image2_' + i +
                                '" src="' + face_obj['base64'] + '" alt="Faces"></div>');
                            $("#face_image2_" + i).css("max-height", height2 + "px");
                            $("#face_imgpad2_" + i).css("height", height2 + "px");
                            $("#face_image2_" + i).css("max-width", height2 + "px");
                            $("#face_imgpad2_" + i).css("width", height2 + "px");
                            if ($("#face_image2_" + i).width() > $("#face_image2_" + i).height()) {
                                $("#face_image2_" + i).css("margin-top",
                                    (height2 - $("#face_image2_" + i).height()) / 2 + "px");
                                $("#face_image2_" + i).css("width", width2);
                            } else {
                                $("#face_image2_" + i).css("height", height2);
                            }
                            $("#face_image2_" + i).click(function () {
                                augment_img_id = '#' + $(this).attr("id");
                                console.log('click ' + augment_img_id);
                            });

                        }
                    };

                } else {
                    alert(response_obj["info"]);
                }

            } else {
                alert("Error: " + XMLHttpRequest.status + " " + textStatus);
            }
        },
        type: "POST",
        global: false,
        contentType: "application/x-www-form-urlencoded",
        dataType: "json"
    });

    $.ajax({data: {"src": src}});

}

function get_landmark() {
    var src = $(this).attr("src");
    var img = new Image();
    img.src = src;

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        url: "/landmark/",
        complete: function (XMLHttpRequest, textStatus) {
            // alert(XMLHttpRequest.responseText + "\n" + textStatus);
            if (XMLHttpRequest.status === 200) { // Success
                console.log("response=" + XMLHttpRequest.responseText);
                response_obj = JSON.parse(XMLHttpRequest.responseText);

                draw_image(undefined, img);
                for (var i = 0; i < response_obj.length; i++) {
                    draw_landmark(response_obj[i][0], response_obj[i][1]);
                }

            } else {
                if (XMLHttpRequest.status > 0)
                    alert("Error: " + XMLHttpRequest.status + " " + textStatus);
                else
                    alert("Error: " + XMLHttpRequest.status + " Server no response.");

            }
        },
        type: "POST",
        global: false,
        contentType: "application/x-www-form-urlencoded",
        dataType: "json"
    });

    $.ajax({data: {"src": src}});

}

function augment() {
    var augment_type = $(this).text();
    if (augment_img_id === undefined)
        augment_img_id = "#face_image2_1";
    var src = $(augment_img_id).attr("src");
    console.log(src);

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        url: "/augment/",
        complete: function (XMLHttpRequest, textStatus) {
            // alert(XMLHttpRequest.responseText + "\n" + textStatus);
            if (XMLHttpRequest.status === 200) { // Success
                console.log("response=" + XMLHttpRequest.responseText);
                response_obj = JSON.parse(XMLHttpRequest.responseText);
                var img = new Image();
                img.src = response_obj;
                img.onload = function () {
                    $("#aug_result").attr("src", response_obj);
                }

            } else {
                if (XMLHttpRequest.status > 0)
                    alert("Error: " + XMLHttpRequest.status + " " + textStatus);
                else
                    alert("Error: " + XMLHttpRequest.status + " No response from server");

            }
        },
        type: "POST",
        global: false,
        contentType: "application/x-www-form-urlencoded",
        dataType: "json"
    });

    $.ajax({data: {"src": src, "type": augment_type}});

}

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

var csrftoken = getCookie('csrftoken');
