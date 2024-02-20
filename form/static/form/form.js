/*
    사용되는 HTML:
    - form/form.html
*/

if (is_submit) {
    for (let item of answers) {
        let id = item.question.toString();
        let etc = false;
        if (id.endsWith('--etc--')) {
            etc = true;
            id = id.substring(0, id.length - 7);  // remove "--etc--"
        };
        let type = question_type[id];
        let value = item.answer;

        switch (type) {
            case "MULTIPLE_CHOICE":
            case "CHECKBOX": {
                if (etc) {
                    let etcText = document.querySelector(`input[name="${id}--etc--"]`);
                    etcText.value = value;
                    etcText.hidden = false;
                }
                else {
                    if (!Array.isArray(value)) {  // if not array, change to array
                        value = [value]
                    }
                    for (let val of value) {
                        let elements = document.querySelectorAll(`input[name="${id}"][value="${val}"]`)
                        for (let element of elements) {
                            element.checked = true;
                        }
                    }
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
else {
    // handle others
    let etcs = document.querySelectorAll('input[value="--etc--"]')
    for (let etc of etcs) {
        let id = etc.name;
        let etcText = document.querySelector(`input[name="${id}--etc--"]`);
        let others = document.querySelectorAll(`input[name="${id}"]`);
        for (let other of others) {
            other.addEventListener('change', function() {
                if (etc.checked) {
                    etcText.hidden = false;
                } else {
                    etcText.hidden = true;
                }
            })
        }
    }

    for (let require of required) {
        let elements = document.querySelectorAll(`*[name="${require}"]:not([type="checkbox"])`)  // Disable checkbox require temporary
        for (let element of elements) {
            element.required = true;
        }
    }
}

/* textarea height */
function textarea_resize(element) {
    element.style.width = "";
    element.style.height = "";
    element.style.height = element.scrollHeight + "px"
}

for (let element of document.getElementsByTagName('textarea')) {
    textarea_resize(element);
}
