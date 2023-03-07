//var add_start = document.getElementById('add_start');
//var add_end = document.getElementById('add_end');
//var add_number = document.getElementById('add_number');
//var add_repeat = document.getElementById('add_repeat');
//var add_last = document.getElementById('add_last');

//function updateAddDiv() {
//    console.log(add_start.value)
//    console.log(add_end.value)
//    console.log(add_number.value)
//    console.log(add_repeat.value)
//    console.log(add_last.value)
//}

//add_start.value = new Date().toISOString().slice(0, 16);

timetable = document.getElementById('timetable');
function toDate(timeValue) {
    return new Date('Sat Mar 11 2017 ' + timeValue + ':00 GMT+0900 (KST)')
}
function toTimeString(date) {
    let hour = date.getHours();
    let minute = date.getMinutes();
    let str = "";

    if (hour < 10) str += "0" + hour;
    else str += hour;

    str += ":"

    if (minute < 10) str += "0" + minute;
    else str += minute;

    return str;
}


document.getElementById('add_time').onclick = function() {
    try {
        let number = timetable.childNodes.length

    let this_start, this_end, this_number, this_date;
    if (number > 2) {
        let last_prev = timetable.childNodes[number-2]
        let last_next = timetable.childNodes[number-1]

//        console.log(last_prev)
//        console.log(last_next)

        let last_prev_start = toDate(last_prev.childNodes[2].childNodes[0].value)
        // last_prev_end = Date.parse(last_prev.childNodes[2].value)

        let last_next_start = toDate(last_next.childNodes[2].childNodes[0].value)
        let last_next_end = toDate(last_next.childNodes[3].childNodes[0].value)

//        console.log(last_prev_start)
//        console.log(last_next_start)
//        console.log(last_next_end)

        this_start = new Date(last_next_start.getTime() + (last_next_start.getTime() - last_prev_start.getTime()))
        this_end = new Date(last_next_end.getTime() + (last_next_end.getTime() - last_next_start.getTime()))

        this_number = last_next.childNodes[4].childNodes[0].value
        this_date = last_next.childNodes[1].childNodes[0].value
    }
    else {
        this_start = new Date()
        this_end = new Date()
        this_number = 1
        this_date = '2023-03-01'
    }

//    console.log(this_date)

    this_start = toTimeString(this_start)
    this_end = toTimeString(this_end)

    timetable.insertAdjacentHTML('beforeend',
    `<tr><td><input type="hidden" name="current" value="0">${number}</td><td><input type='date' name='date' value='${this_date}'></td><td><input type='time' name='start' value='${this_start}'></td><td><input type='time' name='end' value='${this_end}'></td><td><input type='number' name='number' min='0' style='width: 50px;' value='${this_number}'></td></tr>`)
    } catch (e) {
        console.error(e)
    }
    return false;
}

function on_submit() {
    if (!confirm('면접 시간은 최대한 한번에 정해주세요. 나중에 면접 시간 추가는 가능하지만, 삭제는 불가능해요ㅠㅠ 지금 입력한 대로 면접 시간을 설정할까요?')) {
        return false;
    }
    try {
    let lst = [];
//    console.log(timetable.childNodes);
    for (let tr of timetable.childNodes) {
        if (tr.tagName != "TR") continue;
        let obj = {};
        for (let td of tr.childNodes) {
            let elem = td.childNodes[0];
            if (elem.name) {
                obj[elem.name] = elem.value;
            }
        }
        lst.push(obj);
    }
//    console.log(lst);
    document.getElementById('time_data').value = JSON.stringify(lst);

//    return false;
    } catch (e) {
        console.error(e);
        return false;
    }
    return true;
}
