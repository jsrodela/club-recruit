// Nav Selection
function changeNav(element, link) {
    document.querySelector('nav > ul > li.selected').classList.remove('selected')
    element.classList.add('selected')

    wrapper = $('.wrapper')
    wrapper.addClass('fade')
    setTimeout(function() {
        wrapper.load(link + ' .wrapper2', function() {
        history.pushState({page_id: 1}, '', link)
        setTimeout(function() {
            wrapper.removeClass('fade')
        }, 100) // 0.1s to apply style
        })
    }, 300) // 0.3s to fadeout


}