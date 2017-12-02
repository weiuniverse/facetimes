var c, ctx;
var draw_width, draw_height, ratio = 1;

function canvas_load() {
    c = document.getElementById("image_canvas");
    ctx = c.getContext("2d");
    draw_width = c.getAttribute("width");
    draw_height = c.getAttribute("height");
    default_canvas();
}

function default_canvas(img) {
    c.height = c.height;
    if (img === undefined)
        img = document.getElementById("default_img");
    var width = c.getAttribute("width");
    var height = c.getAttribute("height");

    draw_image(undefined, img);
}

function draw_image(e, img) {
    if (img === undefined) {
        id = $(this).attr("id");
        img = document.getElementById(id);
    }

    var width = c.getAttribute("width");
    var height = c.getAttribute("height");
    console.log(img.width + "," + img.height);

    if (img.width >= img.height) {
        draw_width = width;
        ratio = width / img.width;
        draw_height = img.height * ratio;
    } else {
        draw_height = height;
        ratio = height / img.height;
        draw_width = img.width * ratio;
    }
    ctx.drawImage(img, 0, 0, draw_width, draw_height);
}

function draw_face(x, y, w, h) {
    // Note: x, y, w, h are real position of image
    ctx.strokeStyle = "green";
    ctx.strokeRect(x * ratio, y * ratio, w * ratio, h * ratio)
}

function draw_landmark(px, py) {
    ctx.beginPath();
    ctx.arc(px*ratio, py*ratio, 2, 0, Math.PI * 2, true);
    ctx.closePath();
    ctx.fillStyle = 'rgba(0,255,0,0.9)';
    ctx.fill();
}