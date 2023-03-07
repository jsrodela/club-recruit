function onTimeClick(element) {
    if (!confirm(element.name + ' 으로 선택하시겠습니까?')) {
        return false;
    }

    document.getElementById('time_value').value = element.name;
    document.getElementById('time_form').submit();
}