var augment_img_id = undefined;
var focus = [];
var upload_flag = false;
var landmark_flag = false;

function load() {
    resize_callback();

    $("#default_img_list>div").click(upload_default);
    $("#download_btn").click(download_aug_image);
    $('#file').change(function () {
        upload();
    });
    $(".aug_btn").click(augment);
    $(window).resize(resize_callback);
    $("#random_btn").click(random_image);

    focus = [-1, -1, -1];
    $('#collapseOne').on('shown.bs.collapse', function () {
        var img = new Image();
        img.src = $("#default_img").attr("src");
        response_obj = JSON.parse($("#response_json").text());

        img.onload = function () {
          offset = draw_image(undefined, img);
          for (var i = 1; i <= response_obj["faces_list"].length; i++) {
              face_obj = response_obj["faces_list"][i - 1];
              console.log(face_obj);
              draw_face(face_obj['pt_x'], face_obj['pt_y'], face_obj['width'], face_obj['height'], offset);
          }
        };
    });

    $('#collapseTwo').on('shown.bs.collapse', function () {
        id = "#" + $('#collapseTwo>div>.sscroll-bar').attr("id");
        console.log(id);
        init_bar(id);
    });
    $('#collapseThree').on('shown.bs.collapse', function () {
        id = "#" + $('#collapseThree>div>.sscroll-bar').attr("id");
        focus[2] = 0;
        init_bar(id);
        var img = new Image();
        img.src = $("#face_image2_" + (focus[2] + 1)).attr("src");
        offset = draw_image(undefined, img);

    });

    $('#myModal').on('show.bs.modal', function () {
      camera_on();
    });

    canvas_load();
}

function resize_callback() {
    $("#image_canvas").css("width",
        document.getElementById("image").offsetWidth - 30);// 30 is margin-left + margin_right
    $("#image_canvas").css("height",
        document.getElementById("image_canvas").offsetWidth);
    $("#loading_canvas").css("display", "none");
    console.log($("#image").height(), $(".panel-heading:eq(0)").outerHeight(true));
    $("#response_json>pre").css("max-height",
        $("#image").height() - 44 -
        44 - $(".panel-heading:eq(0)").outerHeight(true) - 63);
    scroll_load();

}

function upload() {
    var form = new FormData();

    if (upload_flag) {
        console.info("Heyyyy! Invalid operation...");
        return;
    }

    upload_flag = true;
    $("#face_image_list1").empty();
    $("#face_image_list2").empty();
    $(".aug_btn").addClass("disabled");

    loading_canvas();
    $("#loading_canvas").css("display", "block");
    $("#loading_canvas").css("left", ($("#image_canvas").width() - 360) / 2);
    $("#loading_canvas").css("top", ($("#image_canvas").width() - 360) / 2 + "px");
    $("#gender").text("N/A");
    $("#pname").text("N/A");
    $("#smile").text("N/A");
    $("#glasses").text("N/A");
    $("#pose").text("N/A");

    focus[1] = -1;
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
        "dataType": "text",
        "mimeType": "multipart/form-data",
        "data": form
    };

    $.ajax(settings).done(function (response) {
        console.log(response);
        response_obj = JSON.parse(response);
        if (response_obj["rs"] === "Success") {
            var img = new Image();
            img.src = response_obj["info"];
            $("#default_img").attr("src", img.src);

            img.onload = function () {
                upload_callback(img, response);
                $("#loading_canvas").css("display", "none");
                upload_flag = false;
            };

        } else {
            alert(response_obj["info"]);
            $("#response_json pre").text(json_format(response));
            $("#loading_canvas").css("display", "none");
            upload_flag = false;

        }

    });
}

function upload_default(e, random_idx) {
    var src, idd;
    if (random_idx === undefined) {
        src = $(this).children("img").attr("src");
        idd = $(this).attr("id");
        idx = getidxbyid("#" + $("#" + idd)[0].parentNode.parentNode.id);
        changefocus(idx, $(this).index());
    } else {
        src = $("#default_img_" + (random_idx + 1)).attr("src");
    }
    var i = 1;
    if (upload_flag) {
        console.info("Heyyyy! Invalid operation...");
        return;
    }

    upload_flag = true;
    $("#face_image_list1").empty();
    $("#face_image_list2").empty();
    $(".aug_btn").addClass("disabled");


    loading_canvas();
    $("#loading_canvas").css("display", "block");
    $("#loading_canvas").css("left", ($("#image_canvas").width() - 360) / 2);
    $("#loading_canvas").css("top", ($("#image_canvas").width() - 360) / 2 + "px");
    focus[1] = -1; // It should be writen as focus[getidxbyid(idd)] = -1
    $("#gender").text("N/A");
    $("#pname").text("N/A");
    $("#smile").text("N/A");
    $("#glasses").text("N/A");
    $("#pose").text("N/A");

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        url: "/upload_default/",
        complete: function (XMLHttpRequest, textStatus) {
            if (XMLHttpRequest.status === 200) { // Success
                response_obj = JSON.parse(XMLHttpRequest.responseText);
                if (response_obj["rs"] === "Success") {
                    var img = new Image();
                    img.src = response_obj["info"];
                    $("#default_img").attr("src", img.src);
                    img.onload = function () {
                        upload_callback(img, XMLHttpRequest.responseText);
                        $("#loading_canvas").css("display", "none");
                        upload_flag = false;

                    };

                } else {
                    $("#response_json pre").text(json_format(XMLHttpRequest.responseText));
                    alert(response_obj["info"]);
                    $("#loading_canvas").css("display", "none");
                    upload_flag = false;

                }

            } else {
                $("#response_json pre").text(json_format(XMLHttpRequest.responseText));
                alert("Error: " + XMLHttpRequest.status + " " + textStatus);
                $("#loading_canvas").css("display", "none");
                upload_flag = false;

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
    var idd = $(this).attr("id");
    var src = $("#" + idd + ">img").attr("src");
    var img = new Image();
    img.src = src;

    if (landmark_flag) {
        console.info("Heyyyy! Invalid operation...");
        return;
    }

    landmark_flag = true;

    $("#gender").text("Processing...");
    $("#pname").text("Processing...");
    $("#smile").text("Processing...");
    $("#glasses").text("Processing...");
    $("#pose").text("Processing...");

    console.log("#" + $("#" + idd)[0].parentNode.parentNode.id);
    idx = getidxbyid("#" + $("#" + idd)[0].parentNode.parentNode.id);
    changefocus(idx, $(this).index());

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        url: "/landmark/",
        complete: function (XMLHttpRequest, textStatus) {
            landmark_flag = false;

            if (XMLHttpRequest.status === 200) { // Success
                // console.log("response=" + XMLHttpRequest.responseText);
                response_obj = JSON.parse(XMLHttpRequest.responseText);

                offset = draw_image(undefined, img);
                for (var i = 0; i < response_obj["landmark"].length; i++) {
                    draw_landmark(response_obj["landmark"][i][0], response_obj["landmark"][i][1], offset);
                }
                $("#gender").text(response_obj["gender"]);
                $("#pname").text(response_obj["name"]);
                $("#smile").text(response_obj["smile"]);
                $("#glasses").text(response_obj["glass"]);
                $("#pose").text(response_obj["pose"]);


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
    console.log($(this).index());
    cl = $(".aug_btn:eq(" + $(this).index() + ")")[0].classList;
    if (cl[cl.length - 1] === "disabled") { // inactive operation
        console.info("Heyyyy! Invalid operation...");

        return;
    }

    if (focus[2] === undefined || focus[2] < 0)
        augment_img_id = "#face_image2_1";

    var src = $("#face_image2_" + (focus[2] + 1)).attr("src");

    $("#aug_result").attr("src", "/static/image/loading_cubes_2.gif");
    $(".aug_btn").addClass("disabled");
    $("#download_btn").addClass("disabled");

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
                response_obj = JSON.parse(XMLHttpRequest.responseText);
                var img = new Image();
                img.src = response_obj;
                img.onload = function () {
                    $("#aug_result").attr("src", response_obj);
                    $("#download_btn").removeClass("disabled");
                    $(".aug_btn").removeClass("disabled");

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

function changefocus(idx, val) {
    console.log("idx=" + idx + " val=" + val + " focus[idx]=" + focus[idx]);
    console.log($(id_list[idx] + ">div>div:eq(" + focus[idx] + ")"));
    $(id_list[idx] + ">div>div:eq(" + focus[idx] + ")").removeClass("sscroll-imgpad-active");
    $(id_list[idx] + ">div>div:eq(" + focus[idx] + ")").addClass("sscroll-imgpad-halfactive");

    focus[idx] = val;

    $(id_list[idx] + ">div>div:eq(" + focus[idx] + ")").removeClass("sscroll-imgpad-halfactive");
    $(id_list[idx] + ">div>div:eq(" + focus[idx] + ")").addClass("sscroll-imgpad-active");

}

function upload_callback(img, response_text) {
    offset = draw_image(undefined, img);
    $("#face_image_list1").empty();
    $("#face_image_list2").empty();
    if (response_obj["faces_list"].length == 0) {
        alert("No face found.");
        $(".aug_btn").addClass("disabled");
        $("#response_json pre").text(json_format(response_text));
    }
    else {
        display_obj = JSON.parse(response_text);
        for (i = 0; i < display_obj['faces_list'].length; i++) {
            delete display_obj['faces_list'][i]["base64"];
        }
        $("#response_json>pre").css("max-height",
            $("#image").height() - 44 -
            44 - $(".panel-heading:eq(0)").outerHeight(true) - 63);

        $("#response_json pre").text(json_format(JSON.stringify(display_obj)));
        $(".aug_btn").removeClass("disabled");

        height = $("#face_image_list1").height();
        width = $("#face_image_list1").width();
        height2 = $("#face_image_list2").height();
        width2 = $("#face_image_list2").width();

        init_bar(id_list[1]);
        init_bar(id_list[2]);

        for (var i = 1; i <= response_obj["faces_list"].length; i++) {
            face_obj = response_obj["faces_list"][i - 1];
            console.log(face_obj);
            draw_face(face_obj['pt_x'], face_obj['pt_y'], face_obj['width'], face_obj['height'], offset);
            // Set properties of #face_image_list1
            $("#face_image_list1").append(
                '<div class="sscroll-imgpad sscroll-imgpad-halfactive" id="face_imgpad_' + i + '">' +
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
            $("#face_imgpad_" + i).click(get_landmark);

            // Set properties of #face_image_list2
            $("#face_image_list2").append(
                '<div class="sscroll-imgpad sscroll-imgpad-halfactive" id="face_imgpad2_' + i + '">' +
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
            $("#face_imgpad2_" + i).click(function () {
                idx = getidxbyid("#" + $(this)[0].parentNode.parentNode.id);
                var img = new Image();
                img.src = $("#face_image2_" + ($(this).index() + 1)).attr("src");
                offset = draw_image(undefined, img);
                changefocus(idx, $(this).index());
            });

        }
        display(id_list[1]);
        display(id_list[2]);
        check_btn_display(id_list[1]);
        check_btn_display(id_list[2]);
    }
}

function download_aug_image() {
    var src = $("#aug_result").attr("src");
    cl = $("#download_btn")[0].classList;
    if (cl[cl.length - 1] === "disabled") {
        console.info("Heyyyy! Invalid operation...");
        return;
    }

    if (src.indexOf("data:image/jpg;base64,") === 0) {
        $("#download_img64").val(src);
        $("#aug_form").submit();
    } else
        $("#download_btn").addClass("disabled");
}

function random_image() {
    var r = Math.floor(Math.random() * ($("#default_img_list>div").length));
    focus[0] = -1;
    display(id_list[0]);
    upload_default(undefined, r);

}

function json_format(text_value) {
    if (text_value === "") {
        return "";
    } else {
        var res = "";
        for (var i = 0, j = 0, k = 0, ii, ele; i < text_value.length; i++) {//k:缩进，j:""个数
            ele = text_value.charAt(i);
            if (j % 2 == 0 && ele == "}") {
                k--;
                for (ii = 0; ii < k; ii++) ele = "    " + ele;
                ele = "\n" + ele;
            }
            else if (j % 2 == 0 && ele == "{") {
                ele += "\n";
                k++;
                for (ii = 0; ii < k; ii++) ele += "    ";
            }
            else if (j % 2 == 0 && ele == ",") {
                ele += "\n";
                for (ii = 0; ii < k; ii++) ele += "    ";
            }
            else if (ele == "\"") j++;
            res += ele;
        }
        return res;
    }
}

function camera_on() {
    Webcam.set({
        width: 320,
        height: 240,
        image_format: 'jpeg',
        jpeg_quality: 90
    });
    Webcam.attach( '#my_camera' );
}

function take_snapshot() {
  // take snapshot and get image data
  Webcam.snap( function(data_uri) {
    // display results in page
    $("#default_img").attr("src", data_uri);
    $('#myModal').modal('hide');
    camera_down();
    focus[0] = -1;
    display(id_list[0]);
    upload_snapshot(data_uri);
    // document.getElementById('results').innerHTML =
    //   '<h2>Here is your image:</h2>' +
    //   '<img src="'+data_uri+'"/>';
  } );
}

function camera_down() {
  Webcam.reset();
}

function upload_snapshot(src) {
  var idd;
  var i = 1;
  if (upload_flag) {
      console.info("Heyyyy! Invalid operation...");
      return;
  }

  upload_flag = true;
  $("#face_image_list1").empty();
  $("#face_image_list2").empty();
  $(".aug_btn").addClass("disabled");


  loading_canvas();
  $("#loading_canvas").css("display", "block");
  $("#loading_canvas").css("left", ($("#image_canvas").width() - 360) / 2);
  $("#loading_canvas").css("top", ($("#image_canvas").width() - 360) / 2 + "px");
  focus[1] = -1; // It should be writen as focus[getidxbyid(idd)] = -1
  $("#gender").text("N/A");
  $("#pname").text("N/A");
  $("#smile").text("N/A");
  $("#glasses").text("N/A");
  $("#pose").text("N/A");

  $.ajaxSetup({
      beforeSend: function (xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      },
      url: "/upload_snapshot/",
      complete: function (XMLHttpRequest, textStatus) {
          if (XMLHttpRequest.status === 200) { // Success
              response_obj = JSON.parse(XMLHttpRequest.responseText);
              if (response_obj["rs"] === "Success") {
                  var img = new Image();
                  img.src = response_obj["info"];
                  $("#default_img").attr("src", img.src);
                  img.onload = function () {
                      upload_callback(img, XMLHttpRequest.responseText);
                      $("#loading_canvas").css("display", "none");
                      upload_flag = false;

                  };

              } else {
                  $("#response_json pre").text(json_format(XMLHttpRequest.responseText));
                  alert(response_obj["info"]);
                  $("#loading_canvas").css("display", "none");
                  upload_flag = false;

              }

          } else {
              $("#response_json pre").text(json_format(XMLHttpRequest.responseText));
              alert("Error: " + XMLHttpRequest.status + " " + textStatus);
              $("#loading_canvas").css("display", "none");
              upload_flag = false;

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

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

var csrftoken = getCookie('csrftoken');
