
var banners = document.querySelectorAll('.banner')
var upper_container = document.querySelector('.upper_container');
var current_banner;

function get_random_banner() {
    let random_number = 1000;
    while (true) {
        random_number = Math.floor(Math.random()*banners.length);
        if (0 <= random_number < banners.length && banners[random_number] != current_banner) break;
    }
//    console.log(random_number)
//    console.log(banners[random_number])
    return banners[random_number];
}

function change_banner() {
    var new_banner = get_random_banner();
    new_banner.style = `transition-duration: 0s; transition-duration: 0.5s; margin-left: ${upper_container.offsetWidth}px;`; // 왼쪽으로 옮기고
    current_banner.style = `transition-duration: 0.5s; margin-left: -${upper_container.offsetWidth}px;`; // 오른쪽으로 애니메이션
    new_banner.style = `transition-duration: 0.5s; margin-left: 0px;`; // 가운데로 애니메이션

    setTimeout(function() {
        current_banner.style = "display: none;"
        current_banner = new_banner;
    }, 500)

    /*var banner = document.querySelector('#banner');

    var internal_banner = banner.cloneNode(true);
    upper_container.appendChild(internal_banner);
    internal_banner.id="internal_banner";
    $("#internal_banner").load(location.href + " #banner");
    internal_banner.id="banner";


    internal_banner.style = `margin-left: -${upper_container.offsetWidth}px;`;

    banner.style = `transition-duration: 0.5s; margin-left: ${upper_container.offsetWidth}px;`;

    internal_banner.style = `transition-duration: 0.5s; margin-left: 0px;`;

    setTimeout(function(){
        banner.remove();
    }, 500);*/
    /*setTimeout(function(){
        internal_banner.id="banner";
        banner.remove();
    }, 2000);*/
    //setTimeout(function() {$("#banner").load(location.href + " #banner");}, 1000)
}

function CancelAlert(club_code) {
    if (!confirm("정말로 면접시간 선택을 취소하시겠어요?")) {
        return false
    }
    location.href = '/form/cancel/' + club_code
}

function enterClub(club_code, club_name) {
    if (!confirm(`정말로 ${club_name} 동아리에 가입할까요?\n!! 선택 후 다른 동아리로 변경이 불가합니다! !!`)) {
        return false
    }
    if (!confirm(`정말로 ${club_name} 동아리를 선택할까요?\n!! 지원한 다른 동아리들은 자동으로 포기 처리되며, 이후 되돌릴 수 없습니다! !!`)) {
        return false
    }
    let expected = `${user_id} ${user_name} ${club_name}`;
    let signature = prompt(`학번, 이름, 동아리 이름을 아래와 일치하도록 정확하게 입력해주세요.\n\n ${expected}`);

    // 띄어쓰기 제거 및 소문자 치환
    if (expected.replace(/ /g,'').toLowerCase() != signature.replace(/ /g,'').toLowerCase()) {
        alert(`가입 확인 입력이 잘못되었습니다. 가입 버튼을 다시 눌러주세요.\n\n올바른 입력: ${expected}\n사용자의 입력: ${signature}`);
        return false;
    }

    location.href = 'form/select/' + club_code + '?signature=' + signature;
    return true;
}

current_banner = get_random_banner();
current_banner.style = 'display: block;'

// banner_club query가 있으면 전환 안하기
var params = new Proxy(new URLSearchParams(window.location.search), {
  get: (searchParams, prop) => searchParams.get(prop),
});
console.log(params.banner_club)
if (params.banner_club) {
    let new_banner = document.querySelector(`.banner-${params.banner_club}`)
//    console.log(new_banner);
    if (new_banner != undefined) {
        current_banner.style = 'display: none;'
        current_banner = new_banner;
        current_banner.style = 'display: block;'
    }
}
else {
    // remove previous interval if exists
    if (typeof current_interval !== 'undefined') {
        clearInterval(current_interval)
    }
    var current_interval = setInterval(change_banner, 5000);
}
