function onTimeClick(element) {
    if (!confirm(element.name + ' 으로 선택할까요? 시간을 한번 선택하면 다시 변경할 수 없어요.')) {
        return false;
    }

    document.getElementById('time_value').value = element.name;
    document.getElementById('time_form').submit();
}