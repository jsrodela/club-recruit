


setInterval(function() {
    var upper_container = document.querySelector('.upper_container');
    var banner = document.querySelector('#banner');

    var internal_banner = banner.cloneNode(true);
    upper_container.appendChild(internal_banner);
    internal_banner.id="internal_banner";
    $("#internal_banner").load(location.href + " #banner");
    internal_banner.id="banner";


    internal_banner.style = `margin-left: -${upper_container.offsetWidth}px;`;

    banner.style = `transition-duration: 0.5s; margin-left: ${upper_container.offsetWidth}px;`;

    internal_banner.style = `transition-duration: 0.5s; margin-left: 0px;`;

    setTimeout(function(){
        banner.remove();
    }, 500);
    /*setTimeout(function(){
        internal_banner.id="banner";
        banner.remove();
    }, 2000);*/
    //setTimeout(function() {$("#banner").load(location.href + " #banner");}, 1000)
}, 7000);



