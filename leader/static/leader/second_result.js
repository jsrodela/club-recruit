
let titles = ['pass1', 'pass2'];

for (let title of titles) {
    let form = document.getElementById(title + '_form');
//    let rank = document.getElementById(title + '_rank');
    let user_id = document.getElementById(title + '_user_id');
    let user_name = document.getElementById(title + '_user_name');
    let submit  = document.getElementById(title + '_submit');
    let table = document.getElementById(title + '_table');
    let tbody = document.getElementById(title + '_tbody');

    form.onsubmit = function(event, form) {
        event.preventDefault();
        if (!user_id.value.length || !user_name.value.length) return false;

        if (check_tables(user_id.value)) {
            alert(`'${user_id.value} ${user_name.value}' 학생은 이미 명단에 존재합니다.`);
            return false;
        }

        submit.disabled = true;

        fetch('/leader/second_result_check_user', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            redirect: 'error',
            body: JSON.stringify({
                'user_id': user_id.value,
                'user_name': user_name.value,
            })
        })
            .then((response) => response.json())
            .then((result) => {
                console.log(result);
                if ('error' in result) {
                    alert(result['error']);
                }
                else {
                    let value = `<tr><td>${result['user_id']}</td><td>${result['user_name']}</td><td><a href="/form/leader/${result['form_id']}" target="_blank">보기</a></td><td><button onclick="remove_row(this);">취소</button></td></tr>`;
                    tbody.insertAdjacentHTML('beforeend', value);
                    sort_table(table); user_id.value = "";
                    user_name.value = "";
                    user_id.focus();
                }

                submit.disabled = false;
            })
            .catch((err) => {
                console.log(err);
                alert('서버와 통신하지 못헀어요. 다시 시도해보거나, 이 문제가 지속되면 로델라 부장에게 알려주세요.');
                submit.disabled = false;
            })
        return false;
    }
}

// 명단에 해당 유저가 확인하는지 존재
// number: string = 학번
function check_tables(number) {
    for (let title of titles) {
        let table = document.getElementById(title + '_table');
        for (let row of table.rows) {
            let val = row.cells[0].innerHTML;
            if (number == val) return true;
        }
    }
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


function send_submit() {

    let data = [];
    for (let title of titles) {
        data.push(collect_datas(title));
    }

    if (!data[0].length) {
        alert('합격자 명단이 입력되지 않았습니다.');
        return false;
    }

    let msg = "※ 확인 버튼을 누르고 난 뒤에는 명단을 수정할 수 없습니다. 명단을 다시 한 번 정확히 확인하세요.\n";


    for (let i=0;i<2;i++) {
        msg += '\n● ' + (i+1) + '학년 합격자: ' + data[i].length + '명\n'

        for (let obj of data[i]) {
            msg += `- ${obj['user_id']} ${obj['user_name']}\n`;
        }
    }

    msg += '\n위 명단이 확실한가요?\n명단에 오류가 있다면 취소 버튼을 누른 뒤 수정해주세요.\n확인 버튼을 누르고 난 뒤에는 명단을 수정할 수 없습니다.\n명단을 확정하려면 확인 버튼을 눌러주세요.'

    if (!confirm(msg)) return false;

    console.log(data);
    document.querySelector('input[name="result_data"]').value = JSON.stringify(data);

    return true;
}

function collect_datas(table_id) {
    let table = document.getElementById(table_id + '_table');
    let data = [];
    for (let i=1;i<table.rows.length;i++) {
        let row = table.rows[i];
        // console.log(table_id, d);
        data.push({
            'user_id': row.cells[0].innerHTML,
            'user_name': row.cells[1].innerHTML
        })
    }
    return data;
}