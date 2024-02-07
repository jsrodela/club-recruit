# 개발환경 준비

`이렇게 생긴 박스` 안에 있는 명령어는 명령 프롬프트(cmd)에 입력해야 합니다. 명령 프롬프트는 Win+S로 검색창을 열어 cmd를 입력하면 실행할 수 있습니다.
```
이렇게 생긴 박스의 명령어도 명령 프롬프트에서 실행해주세요.
```
> 가끔 `python` 명령어가 작동하지 않으면, 대신 `python3`를 입력해보세요.

### 1. 필요 프로그램

* Python 3.9 이상 (필수)
  * https://www.python.org/downloads/
  * `python --version` 입력하여 버전 확인 가능
* Pip (필수)
  * `python -m ensurepip --upgrade`로 설치
* Pycharm Community
  * 파이썬 코딩을 도와주는 프로그램. 무료인 Community 버전으로 다운받기
  * https://www.jetbrains.com/ko-kr/pycharm/download/#section=windows
* Git
  * Github와 연동하여 버전 관리 및 코드 공유를 도와주는 프로그램
  * https://git-scm.com/download/win 에서 'Click here to download' 눌러서 설치
  * `git --version`으로 설치 확인 가능

### 2. 소스코드 복제
```commandline
git clone https://github.com/RoDeLa6/club-recruit
cd club-recruit
```

### 3. 개발 환경 준비

> Pycharm 사용 시, 이 설정을 완료한 뒤 우측 하단 `<No Interpreter>` -> Add Interpreter -> OK 눌러주면 더 간편하게 가상 환경을 사용할 수 있습니다.

```commandline
python -m venv .venv
.venv/Scripts/activate
```
> Linux에서는 두번째 명령어를 `. .venv/bin/activate`로 입력해야 합니다.

가상 환경을 생성한 후, 아래 명령어를 입력하여 필요한 모듈을 설치해줍니다.
> Pycharm의 경우 하단의 Terminal 메뉴에서 입력해보세요.
```commandline
pip install -r requirements.txt
```

### 4. 장고 서버 설정

`settings-example.json`을 복사하여 `settings.json`로 이름을 바꾸고, 내용을 알맞게 수정해주세요.
```json
{
  "extform_url": "https://script.google.com/macros/s/.../exec",
  "secret_key": "django-insecure-=jwym+hlrxql772fu&(*^20cyt%_8t4wu$^dw__v^ugbm*=+ha",
  "allowed_hosts": ["localhost", "127.0.0.1"],
  "production": false
}
```
그리고 아래 명령어를 통해 서버 DB를 동기화한 후, 서버를 열어줍니다.
> Pycharm 사용 시, 대신 우측 위의 실행 메뉴를 사용할 수도 있습니다.
```commandline
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
서버가 정상적으로 열렸다면 웹브라우저에서 `127.0.0.1:8000` 으로 접속하여 실행된 상태를 볼 수 있습니다.

> 동아리가 2개 이상 존재하지 않으면 무한 로딩이 걸리는 버그가 있습니다. `python manage.py createsuperuser`로 관리자 계정을 생성하고, /admin 주소로 접속하여 동아리를 2개 추가해주세요.