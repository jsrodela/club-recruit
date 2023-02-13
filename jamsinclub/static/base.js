// Nav Selection
// code: nav에서 .select할 class
// link: location.href

function changeNav(code, link) {
    selectNav(code);

    let wrapper = document.querySelector('.wrapper');
    wrapper.classList.add('fade');
    setTimeout(function() {
        fetch(link)
            .then(response => response.text())
            .then(text => {

                // get wrapper
                let temp = new DOMParser().parseFromString(text, "text/html");
                let fetched_wrapper = temp.querySelector('.wrapper2');
                document.querySelector('.wrapper2').innerHTML = fetched_wrapper.innerHTML;

                // run scripts manually
                // exclude <script src=...> and <script type="text/markdown"> (already executed via innerHTML)
                for (let script of fetched_wrapper.querySelectorAll("script:not([src],[type='text/markdown'])")) {
                    try {
                        eval(script.innerHTML);
                    }
                    catch (err) {
                        console.error(err)
                    }
                }

                // change location.href without reload (뒤로가기 제외)
                if (code != '__popstate__')
                    history.pushState({page_id: 1}, '', link)

                // register smooth reload on every <a>
                register_onclick();

                // show element after 0.1s
                setTimeout(function() {
                    wrapper.classList.remove('fade');
                }, 100);
            })
    }, 300) // 0.3s to fadeout

    return false;
}

function selectNav(code) {
    console.log(code)
    if (code == '' || code == '__popstate__') return;
    for (let element of document.querySelectorAll('nav > ul > li.selected')) {
        element.classList.remove('selected');
    }
    document.querySelector('nav > ul > li.' + code).classList.add('selected')
}

function register_onclick() {
    // for every <a>
    links = document.getElementsByTagName('a')
    for (let link of links) {

        if (link.onclick == null && link.href == null) { // if onclick or href is not defined
            link.onclick = function(event) {
                return changeNav('', link.href);
            }
        }
    }
}

// On page loaded
window.addEventListener('load', function() {
    register_onclick()
});

window.addEventListener("popstate", function(event) {
    return changeNav('__popstate__', location.href);
});
