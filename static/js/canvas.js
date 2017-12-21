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
    // draw_image(undefined, img);
    ctx.font = "14px sans-serif";
    text = "Upload an image or pick one from gallery.";
    length = ctx.measureText(text);
    console.log((c.width-length.width)/2+","+(c.height-7)/2);
    ctx.fillText(text, (c.width-length.width)/2, (c.height-7)/2);
}

function draw_image(e, img) {
    c.height = c.height;
    if (img === undefined) {
        id = $(this).attr("id");
        img = document.getElementById(id);
    }

    var width = c.getAttribute("width");
    var height = c.getAttribute("height");
    var w = width, h = height;
    if (img.width * 2.5 < width)
        width = img.width * 2.5;
    if (img.height * 2.5 < height)
        height = img.height * 2.5;

    if (img.width >= img.height) {
        draw_width = width;
        ratio = width / img.width;
        draw_height = img.height * ratio;
    } else {
        draw_height = height;
        ratio = height / img.height;
        draw_width = img.width * ratio;
    }

    ctx.drawImage(img, (w - draw_width) / 2, (h - draw_height) / 2, draw_width, draw_height);
    return [(w - draw_width) / 2, (h - draw_height) / 2]; // Return x_offset and y_offset
}

function draw_face(x, y, w, h, offset) {
    // Note: x, y, w, h are real position of image
    ctx.strokeStyle = "green";
    ctx.strokeRect(x * ratio + offset[0], y * ratio + offset[1], w * ratio, h * ratio)
}

function draw_landmark(px, py, offset) {
    ctx.shadowOffsetX = 1;
    ctx.shadowOffsetY = 1;
    ctx.shadowColor = 'rgba(100,100,100,0.5)';
    ctx.shadowBlur = 1;
    ctx.beginPath();
    ctx.arc(offset[0] + px * ratio, offset[1] + py * ratio, 2, 0, Math.PI * 2, true);
    ctx.closePath();
    ctx.fillStyle = 'hsla(200,100%,40%,1)';
    ctx.fill();
}

function loading_canvas() {
    c.height = c.height;
    ctx.fillStyle = "#eaeaea";
    ctx.fillRect(0,0,c.width, c.height);
}