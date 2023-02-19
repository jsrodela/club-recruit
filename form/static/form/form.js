/*
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

let rad2 = document.querySelectorAll('input[name=984420844]')
let etcText2 = document.querySelector('input[name=984420844-etc]')
for (let i of rad2) {
    i.addEventListener('change', function() {
        if (i.value == '{{choice.value}}') {
            etcText2.hidden = false;
        } else {
            etcText2.hidden = true;
        }
    })
}
*/

if (is_submit) {
    for (let item of answers) {
        let id = item.question.toString();
        if (id.endsWith('--etc--')) continue;
        let type = question_type[id];
        let value = item.answer;

        switch (type) {
            case "MULTIPLE_CHOICE":
            case "CHECKBOX": {
                let elements = document.querySelectorAll(`input[name="${id}"][value="${value}"]`)
                for (let element of elements) {
                    element.checked = true;
                }
                break;
            }
            case "LIST": {
                let element = document.querySelector(`select[name="${id}"] option[value="${value}"]`)
                element.selected = true;
                break;
            }
            case "TEXT": {
                let element = document.querySelector(`input[name="${id}"]`);
                element.value = value;
                break;
            }
            case "PARAGRAPH_TEXT": {
                let element = document.querySelector(`textarea[name="${id}"]`);
                element.innerHTML = value;
                break;
            }
            default: {
                console.error('Unknown type: ' + type)
                break;
            }
        }
    }
    for (let tagname of ['input', 'textarea', 'select']) {
        for (let element of document.getElementsByTagName(tagname)) {
            if (element.type == 'submit' || element.type == 'hidden') continue; // 지원 취소 버튼 & csrfmiddlewaretoken
            element.disabled = true;
        }
    }
}
