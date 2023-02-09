// Nav Selection
function changeNav(element, link) {
    if (element.tagName == 'LI') {
        document.querySelector('nav > ul > li.selected').classList.remove('selected')
        element.classList.add('selected')
    }

    wrapper = $('.wrapper')
    wrapper.addClass('fade')
    setTimeout(function() {
        wrapper.load(link + ' .wrapper2', function() {
            history.pushState({page_id: 1}, '', link)

            register_onclick();

            setTimeout(function() {
                wrapper.removeClass('fade')
            }, 100) // 0.1s to apply style
        })
    }, 300) // 0.3s to fadeout

    return false;
}

function register_onclick() {
    // for every <a>
    links = document.getElementsByTagName('a')
    for (let link of links) {

        if (link.onclick == null && link.href == null) { // if onclick or href is not defined
            link.onclick = function(event) {
                return changeNav(event.target, link.href);
            }
        }
    }
}

// On page loaded
window.onload = function() {
    register_onclick()
}
