// 급하게 second_result.js 복붙하긴 했는데, 통일성 위해서 나중에 합쳐두면 좋을듯
let form = document.getElementById('form');
let user_id = document.querySelector('input[name="user_id"]');
let user_name = document.querySelector('input[name="user_name"]');
let submit_btn = document.getElementById('submit_btn');

submit_btn.onclick = function(event) {
    if (!user_id.value.length || !user_name.value.length) return false;

    submit_btn.disabled = true;

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
                if (!confirm(`${user_id.value} ${user_name.value} 학생을 추가합격 대상자로 선정할까요?`)) return false;
                form.submit();
                return true;
            }

            submit_btn.disabled = false;
        })
        .catch((err) => {
            console.log(err);
            alert('서버와 통신하지 못헀어요. 다시 시도해보거나, 이 문제가 지속되면 로델라 부장에게 알려주세요.');
            submit_btn.disabled = false;
        })
    return false;
}