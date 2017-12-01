function load() {
    $("#image_canvas").css("width",
        document.getElementById("image").offsetWidth - 30);// 30 is margin-left + margin_right
    $("#image_canvas").css("height",
        document.getElementById("image_canvas").offsetWidth);
    $(".sscroll-img-list img").click(upload_default);
    $('#file').change(function () {
        upload();
    });
    canvas_load();
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
        response_obj = JSON.parse(response);
        if (response_obj["rs"] === "Success") {
            var img = new Image();
            img.src = response_obj["info"];
            img.onload = function () {
                default_canvas(img);
                for (var i = 0; i < response_obj["faces_list"].length; i++)
                    face_obj = response_obj["faces_list"][i]
                draw_face(face_obj['pt_x'], face_obj['pt_y'], face_obj['width'], face_obj['height']);
            };

        } else {
            alert(response_obj["info"]);
        }
    });
}

function upload_default() {
    var src = $(this).attr("src");

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

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
                        for (var i = 0; i < response_obj["faces_list"].length; i++) {
                            face_obj = response_obj["faces_list"][i];
                            console.log(face_obj);
                            draw_face(face_obj['pt_x'], face_obj['pt_y'], face_obj['width'], face_obj['height']);
                        }
                    };

                } else {
                    alert(response_obj["info"]);
                }

            } else {
                alert("Error: "+XMLHttpRequest.status + " " + textStatus);
            }
        },
        type: "POST",
        global: false,
        contentType: "application/x-www-form-urlencoded",
        dataType: "json"
    });

    $.ajax({data: {"src": src}});

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

var csrftoken = getCookie('csrftoken');