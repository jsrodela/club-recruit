let init_form = document.getElementById('init_form');
let init_user_id = document.getElementById('init_user_id');
let init_user_name = document.getElementById('init_user_name');
let init_submit  = document.getElementById('init_submit');
let init_table = document.getElementById('init_table');
let init_tbody = document.getElementById('init_tbody');

init_form.onsubmit = function(event, form) {
    event.preventDefault();

    if (!init_user_id.value.length || !init_user_name.value.length) return false;

    init_submit.disabled = true;

    fetch('/leader/second_result_check_user', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        redirect: 'error',
        body: JSON.stringify({
            'user_id': init_user_id.value,
            'user_name': init_user_name.value
        })
    })
        .then((response) => response.json())
        .then((result) => {
            console.log(result);
            if ('error' in result) {
                alert(result['error']);
            }
            else {
                init_tbody.insertAdjacentHTML('beforeend',
                    `<tr><td>${result['user_id']}</td><td>${result['user_name']}</td><td><a href="/form/leader/${result['form_id']}" target="_blank">보기</a></td><td><button onclick="remove_row(this);">취소</button></td></tr>`);
                sort_table(init_table);
                init_user_id.value = "";
                init_user_name.value = "";
            }

            init_submit.disabled = false;
        })
        .catch((err) => {
            console.log(err);
            alert('서버와 통신하지 못헀어요. 다시 시도해보거나, 이 문제가 지속되면 로델라 부장에게 알려주세요.');
            init_submit.disabled = false;
        })
    return false;
}

function remove_row(element) {
    element.parentElement.parentElement.remove();
}

function sort_table(table) {
  let rows, switching, i, x, y, shouldSwitch;
  switching = true;
  /* Make a loop that will continue until
  no switching has been done: */
  while (switching) {
    // Start by saying: no switching is done:
    switching = false;
    rows = table.rows;
    /* Loop through all table rows (except the
    first, which contains table headers): */
    for (i = 1; i < (rows.length - 1); i++) {
      // Start by saying there should be no switching:
      shouldSwitch = false;
      /* Get the two elements you want to compare,
      one from current row and one from the next: */
      x = rows[i].getElementsByTagName("TD")[0];
      y = rows[i + 1].getElementsByTagName("TD")[0];
      // Check if the two rows should switch place:
      if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
        // If so, mark as a switch and break the loop:
        shouldSwitch = true;
        break;
      }
    }
    if (shouldSwitch) {
      /* If a switch has been marked, make the switch
      and mark that a switch has been done: */
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
    }
  }
}