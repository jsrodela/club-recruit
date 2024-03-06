function onTimeClick(element, msg) {
    if (!confirm(msg + ' 으로 선택할까요?')) {
        return false;
    }

    document.getElementById('time_id').value = element.name;
    document.getElementById('time_form').submit();
}