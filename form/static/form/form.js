let rad = document.querySelectorAll('input[name=c-language]')
let etcText = document.querySelector('input[name=c-language-etc]')
for (let i of rad) {
    i.addEventListener('change', function() {
        if (document.querySelector('input[name=c-language][value=etc]').checked) {
            etcText.hidden = false;
        } else {
            etcText.hidden = true;
        }
    })
}

let rad2 = document.querySelectorAll('input[name=c-language-best]')
let etcText2 = document.querySelector('input[name=c-language-best-etc]')
for (let i of rad2) {
    i.addEventListener('change', function() {
        if (i.value == 'etc') {
            etcText2.hidden = false;
        } else {
            etcText2.hidden = true;
        }
    })
}