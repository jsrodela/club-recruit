// Nav Selection
function changeNav(element, link) {
    document.querySelector('nav > ul > li.selected').classList.remove('selected')
    element.classList.add('selected')

    $('.wrapper').load(link + ' .wrapper2', function() {
        history.pushState({page_id: 1}, '', link)
    })

}