
if (not_done) {
    document.getElementById('check_all').onclick = function(event) {
        document.querySelectorAll('.is_pass').forEach(function(checkbox) {
            checkbox.checked = true;
        })
    }

    document.getElementById('uncheck_all').onclick = function(event) {
        document.querySelectorAll('.is_pass').forEach(function(checkbox) {
            checkbox.checked = false;
        })
    }
}
else {
    let names = ['all', 'pass', 'fail']
    for (let name of names){
        document.getElementById(`copy_${name}_phone`).onclick = function(event) {
            navigator.clipboard.writeText(document.getElementById(`${name}_phone`).innerHTML).then(function() {
                alert("복사 완료!");
            })
        }
    }
}