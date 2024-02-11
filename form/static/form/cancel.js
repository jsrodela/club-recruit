function onTimeClick(element) {
    if (!confirm(element.name + ' 을 취소할까요?')) {
        return false;
    }

    document.getElementById('cancel_value').value = element.name;
    document.getElementById('cancel_form').submit();
}