/*
    사용되는 HTML:
    - about/leader.html
*/

function textarea_resize(element) {
    element.style.height = "";
    element.style.height = element.scrollHeight + "px"
}

for (let element of document.getElementsByTagName('textarea')) {
    textarea_resize(element);
}
