function onTimeClick(element) {
    if (!confirm(element.name + ' 으로 취소할까요?')) {
        return false;
    }

    document.getElementById('time_value').value = element.name;
    document.getElementById('time_form').submit();
}