/*
    사용되는 HTML:
    - about/about.html
*/

// 전역변수는 var
var image_num = 0;

function change_image(delta) {
    if (images.length == 0) return;

    let photo = document.querySelector('.photo');

    let animation_type;
    if (delta > 0) animation_type = 'right';
    else if (delta < 0) animation_type = 'left';
    else animation_type = 'none';

    photo.style = generate_image_style(animation_type + '_out')

    setTimeout(function() {
        image_num += delta;
        if (image_num < 0) image_num += images.length
        else if (image_num >= images.length) image_num -= images.length

        photo.style = generate_image_style(animation_type + '_in')
    }, 500)
//    console.log(images[image_num])
}

function generate_image_style(animation_name) {
    // animation_fill_mode가 처음부터 들어가면 Safari에서 안보이는듯
    return 'animation-name: ' + animation_name + '; --photo-url: url("' + images[image_num] + '"); animation-fill-mode: forwards;'
}

change_image(0);

