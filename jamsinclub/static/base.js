// Nav Selection
function changeNav(element) {
    document.querySelector('nav > ul > li.selected').classList.remove('selected')
    element.classList.add('selected')

    /*$('.wrapper').load('/', function() {
        alert('loaded')
    })
    alert('loading')*/
}