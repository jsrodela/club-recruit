var add_start = document.getElementById('add_start');
var add_end = document.getElementById('add_end');
var add_number = document.getElementById('add_number');
var add_repeat = document.getElementById('add_repeat');
var add_last = document.getElementById('add_last');

function updateAddDiv() {
    console.log(add_start.value)
    console.log(add_end.value)
    console.log(add_number.value)
    console.log(add_repeat.value)
    console.log(add_last.value)
}

add_start.value = new Date().toISOString().slice(0, 16);
