# club-recruit
2023년 잠신고등학교 상설동아리 모집 사이트입니다.

By RoDeLa 6.0

* 개발 환경 설정: [DEV_SETUP.md](DEV_SETUP.md)
* 서버 설정: [PRODUCTION.md](PRODUCTION.md)

=== 보고서 작성중 ===

## 1. 서론
작년에 1학년으로써 동아리에 지원하는 입장이었던 우리는, 인스타그램을 통한 동아리 홍보의 단점을 느꼈다. 올해는 2학년으로써 동아리 부원을 선발하는 위치에 서게 되었고, 작년 방식의 한계점을 극복하기 위해 동아리 통합 지원 사이트를 직접 제작하여 운영하기로 하였다.

## 2. 사전 조사

### 2-1. 기존 진행 방식
2022년의 잠신고 상설동아리 신입부원 모집 방식에는 다음과 같은 문제가 있었다.

1. 

2022년 잠신고에서는 연초에 상설동아리 부원을 모집할 때, 각각 동아리에서 지원 서류(구글 설문지 등)를 만들고, 전용 인스타그램에 올리는 홍보 포스터에 지원 서류 링크로 이동하는 QR코드를 탑재하는 방식으로 진행했다. 그러나 이런 방식에는 다음과 같은 문제점이 있었다.

## 3. 구조 및 설계
### 3-1. 사이트 구조
> `동아리`는 각 동아리의 영문 코드를 말합니다. (예: rodela, asap, book, ...)
- **메인 페이지** (`/`) : 지원한 동아리, 면접 일정, 내 정보 등을 한눈에 볼 수 있는 홈 화면
- **소개 페이지** (`/about/동아리`) : 동아리 소개 사진, 홍보 문구와 '지원하기' 버튼이 있는 화면
- 지원 관련
  - **지원 페이지** (`/form/submit/동아리`): 동아리 지원 양식 작성 화면
  - **지원서 확인 페이지** (`/form/views/동아리`) : 자신이 작성한 지원서를 확인할 수 있는 화면
  - **면접시간 선택 페이지** (`/form/time/동아리`) : 1차 합격자 대상으로 면접 시간을 선택할 수 있는 화면
  - **부장 지원서 확인 페이지** (`/form/leader/지원번호`) : 부장 및 부원들이 `지원번호` 지원서를 확인할 수 있는 화면 (해당 동아리에만 열람 권한 존재)
- 부장 관련
  - **동아리 관리 페이지** (`/leader/club_config`) : 부장 전용 동아리 설정 화면. 동아리 정보, 소개페이지 설정 및 부원 추가 기능
  - **1차 서류 확인 페이지** (`/leader/view_forms`) : 부장 및 부원 전용, 본인 동아리에 제출된 지원서 목록 화면.
  - **면접시간 설정 페이지** (`/leader/time_config`) : 부장 전용 2차 면접시간 설정 화면.
  - **1차 결과 결정 페이지** (`/leader/first_result`) : 

### 3-2. 프로젝트 구조
- about: 소개페이지 관련 / `ClubModel` `ImageModel`
- account: 유저 계정 및 로그인 관련 / `User`
- form: 지원 관련 (1차 지원서 및 2차 면접시간 포함) / `FormModel`
- index: 메인페이지 관련
- jamsinclub: 장고 메인 모듈
- leader: 부장 및 동아리 관리페이지 관련

### 3-3. DB 구조

#### 3-3-1. UserModel
> Django에서 기본 제공하는 `AbstractBaseUser` 클래스를 참조하고 있습니다.
> 
> `PhoneNumberField`는 `django-phonenumber-field` 모듈의 모델입니다.

| 이름        | 설명               | 타입                   | 비고                                                         |
|-----------|------------------|----------------------|------------------------------------------------------------|
| id        | 학번               | PositiveIntegerField | PrimaryKey, Unique, NotNull, NotBlank      |
| name      | 이름               | CharField | MaxLength=5, NotNull, NotBlank                             |
| phone     | 전화번호             |PhoneNumberField| NotNull, NotBlank                                          |
|           |
| leader_of | 해당 동아리의 부장 권한 보유 |ForeignKey (ClubModel)| RelatedName='leader_of+', NullOnDelete, Nullable, Blankable |
| member_of | 해당 동아리의 부원 권한 보유 |ForeignKey (ClubModel)| RelatedName='member_of+', NullOnDelete, Nullable, Blankable |

#### 3-3-2. ClubModel
|변수| 설명                                                       | 타입                           | 비고                                                                   |
|-|----------------------------------------------------------|------------------------------|----------------------------------------------------------------------|
|name| 동아리 이름                                                   | CharField                    | MaxLength=100                                                        |
|code| 동아리 영문 코드                                                | CharField                    | PrimaryKey, Unique, MaxLength=10                                     |
||
|form_start| 1차 지원서 제출 시작 시각                                          | DateTimeField                |                                                                      |
|form_end| 1차 지원서 제출 마감 시각                                          | DateTimeField                |                                                                      |
||
|index_banner_image| 메인페이지 배너 이미지                                             | ForeignKey (ImageModel)      | RelatedName='index_banner_image+', NullOnDelete, Nullable, Blankable |
|index_banner_description| 매인페이지 배너 한줄소개                                            | TextField                    |                                                                      |
|index_banner_color| 메인페이지 배너 글자 색상 (#000000 or #ffffff)                      | CharField                    | MaxLength=7                                                          |
||
|about_background| 소개페이지 배경사진                                               | ImageModel                   | RelatedName='index_banner_image+', NullOnDelete, Nullable, Blankable |
|about_images| 소개페이지 사진칸에 들어갈 사진들                                       | ManyToManyField (ImageModel) | RelatedName='about_images+, Blankable                                |
|about_text| 소개페이지 홍보 문구 (HTML/마크다운 문법 지원)                            | TextField                    |                                                                      |
||
|logo_image| 동아리 로고 (왼쪽 동아리 목록 메뉴에 표시)                                | ForeignKey (ImageModel)      | RelatedName='logo_image+', NullOnDelete, Nullable, Blankable         ||
||
|form_data| 구글폼에서 받아온 1차 지원서 양식 (수동 동기화 필요)                          | JSONField                    | dict 형식                                                              |
|form_edit_url| 구글폼 수정 바로가기 링크                                           | URLField                     | Nullable, Blankable                                                  |
|kakao_url| 지원서 기능 미사용 시, 오픈채팅 등 지원 가능한 외부 링크 (이 값이 존재하면 지원서 기능 비활성화) | URLField                     | Nullable, Blankable                                                  |
|members| 멤버 목록 (지원서, 면접시간 확인 권한) - `User`과 자동 동기화 안됨              | JSONField                    | list 형식                                                              |
||
|time_use| 2차 면접 시간선택 기능 사용 여부 (기본 비활성화, 시간 설정 시 활성화)               | BooleanField                 ||
|time_start| 2차 면접 시간선택 시작 시각| DateTimeField                ||
|time_data|2차 면접 시간 데이터| list 형식                      |
> `form_data` 형식은 ExtForm을 참고하세요.
> 
> `members` 형식은 숫자로 이루어진 리스트입니다. (ex. [10000, 10001, 20124])
> 
> 

## 5. 사이트 운영
### 5-1. 준비 (2023. 02. 18. ~ 2023. 03. 01.)
2월 18일, 상설동아리 부장 톡방을 생성하고, 부장들에게 사이트를 통한 모집 계획을 안내하며 협조를 부탁했다. 물론 처음 해보는 시도인 만큼 부장들 간 약간의 혼란이 있었지만, 서로 의견을 조율하며 각 동아리의 소개페이지와 지원 서류를 꾸렸다. 미리 교장선생님과 창의체험부 부장 선생님께 사이트 이용 허락을 받고, 예비소집일 동아리 홍보 시간에도 1학년 학생들에게 사이트를 안내했다.

### 5-2. 1차 지원 (2023. 03. 02. ~ 2023. 03. 14.)
교실 앞 게시판, 중앙현관 게시판, 정보관 앞 게시판 등 학교 곳곳에 동아리 홍보 포스터를 부착하고, 동아리 지원 사이트에서 지원할 수 있다는 내용을 포함했다. 모든 동아리가 사이트에 소개글을 올리고 지원서 제출을 활성화했으며, 학생들은 각자의 학번으로 가입하여 자신이 원하는 동아리를 살펴보고 지원하였다.

### 5-3. 2차 면접 (2023. 03. 08. ~ 2023. 03. 13.)

### 5-4. 운영 종료 (2023. 03. 19. ~ )
모든 상설동아리 모집이 종료되어, 개인정보 보호 및 해킹 방지를 위해 서버 운영을 마무리하였다. 기존 사이트 형식에 맞춰 운영 종료 안내 페이지를 만들고, 해킹 위험이 있는 가상머신 대신 Github Pages를 이용하여 정적 페이지를 호스팅하였다. 서버의 모든 데이터를 안전한 장소로 옮긴 후 서버를 종료했다. 운영 종료를 알리는 페이지를 제작하여, Github Pages를 이용하여 호스팅하였다.


## 7. 개선할 점

### 7-1. 면접시간 선택 시스템 구조 개선
**내년에도 이 시스템을 사용할 경우, 반드시 개선해야 할 사항이다.**

현재 면접시간 선택 시스템의 구조는 동기화 문제가 일어날 여지가 있다. 지금 구조에서는 각 학생의 `FormModel`과 동아리의 `ClubModel`에 지원 시간이 따로 저장되며, DB상에서 둘이 연결되지 않는다. 만약 두 학생이 같은 시각을 동시에 선택하면, 2개의 `FormModel`에 시간이 기록되지만 `ClubModel`에는 학생 수 카운트가 1만 올라갈 수 있다.

추가로 면접시간을 잘못 선택했을 때를 대비하여, 선택을 수정할 수 있는 시스템을 구축할 필요가 있다. 실제 운영에서는 관리자에게 따로 연락하여 선택한 시간을 취소하는 방법을 사용했는데, 약 30명의 학생이 문의하여 처리가 쉽지 않았다.

하나의 개선 방법으로, 면접 시간에 관한 데이터를 담는 새로운 모델(예:`TimeModel`)을 생성하여, `FormModel`에는 `ForeignKey`로, `ClubModel`에는 `ManyToManyField`로 연결해주는 것을 제안한다. 이렇게 하면 새 `TimeModel`을 생성하고 `FormModel`과 `ClubModel`에 동시에 연결되므로, 동기화 문제뿐만 아니라 선택 취소 기능을 구현하기도 훨씬 수월할 것이다.

### 7-2. 

### 7-?. 기타 사항
- 지원 마감 기한을 소개페이지에 표기 (동아리 부장이 설정한 시간으로)
- Safari 브라우저에서 1차 서류 화면의 '지원하기' 버튼이 너무 작아짐


## 9. 활동 소감


## 10. 일자별 활동 내역

1/17
- 프로젝트 생성

1/21
- Django 프로젝트 시작
- 개발 가이드 작성

1/22
- Pycharm 실행 옵션 추가
- 개발 가이드에 Pycharm 가이드 추가

1/23
- 학생(회원) 모델 추가

1/25
- 로그인, 회원가입 페이지 추가

2/1
- 홈, 소개, 지원 페이지 추가

2/2
- 소개페이지 레이아웃 개선, 사진 칸 추가

2/5
- 화면전환 시 페이드 효과 추가
- 세로로 페이지 넘치던 문제 해결

2/6
- 전체 화면에서 페이지가 화면에 꽉차지 않던 문제 해결
- 비밀번호 분실 페이지 추가
- 로그인, 회원가입 페이지 정리
- 개인정보 안내 문서 추가
- .js가 HTML 로딩 완료 이후에 실행되도록 수정
- 지원페이지 폰트 및 색상, 디자인 수정
- `<a>` 태그에 화면전환 효과 추가
- 페이지 대표색 var.css로 분리 및 변수화
- 예시 설문지 데이터 적용
- 소개페이지 소개글 넓이 수정

2/8
- 왼쪽 메뉴바 홈버튼 더 크게, 메뉴바 여백 개선
- 메인화면에 배너 추가

2/9
- 상단바 로고 비율 변경
- 전반적인 디자인 개선
- `<a>` 태그가 덮어씌워지던 오류 해결
- 모바일 레이아웃 지원 추가

2/10
- 메인페이지 '내 정보' 칸 디자인 개선 (윤곽선 삭제 포함)
- 지원페이지 객관식, 단답, 장문, 섹션 헤더 지원
- 지원페이지 질문 간 구분선 추가
- FormModel 추가
- 지원페이지 장문 textarea로 변경
- 소개페이지 레이아웃 개선
- '지원하기' 클릭 시 FormModel로 처리되도록 기능 적용
- 제출한 지원서 보기 기능 추가

2/12
- 소개페이지 배경이미지 추가
- 소개페이지 이미지 비율 1:1로 변경, 비율 안맞으면 꽉차게 자르도록 설정
- 로그인 안했을 때 홈에서 오류나던거 수정

2/13
- 상단바 글씨 삭제, 로고만 남겨두기
- 메뉴바 동아리 종류 표기 삭제
- 모바일에서 메뉴바 아래로 이동
- ClubModel 추가
- 배너에 글씨 및 소개글, 버튼 추가
- 모델에 주석 추가
- 메뉴바에 실제 ClubModel 반영
- ImageModel 저장 경로 수정
- 소개페이지에 ClubModel 및 마크다운 적용
- 

2/25
- 동아리 관리 페이지에서 지원 시간 모바일에서 설정 못하던 오류 해결 (유엔아이 부장님 제보 감사용)

2/27
- 2차 면접시간 사이트 초안 제작
- 홈 배너에 동아리 이름 하양색으로 변경 가능하도록 수정

2/28
- 카카오톡 및 인스타 DM에서 미리보기 이미지 추가
- Google Search Console에 사이트 등록
- 관리자용 비밀번호 변경 사이트 추가

3/1
- 구글폼에서 줄바꿈한 대로 지원서에서 줄바꿈이 되지 않던 오류 해결 (Ph.D 부장 제보 ㄳ)

3/2
- '개인정보를 처리하는 방법' 및 '문의하기' 내용 업데이트
- input[type=checkbox]에서 required 적용 관련 오류, 임시로 required 적용 예외처리 시킴
- 지원서 목록 페이지에 전화번호 노출
- 동아리 부원 기능 추가, 부원들이 지원서 볼 수 있도록 수정 (부장이 동아리 관리 페이지에서 부원 추가 및 삭제 가능)

3/3
- RoDeLa 4.0 갓 건우선배 피드백 적용
  - 최상단 헤더의 이미지 클릭 시 '홈' 메뉴로 이동
  - 소개페이지 사진 크기가 너비&높이에 모두 맞추도록 수정
  - 소개페이지 사진 애니메이션 잔상이 남던 버그 해결
  - 소개페이지 모바일 전환 기준 수정 (768px -> 1024px)
  - 소개페이지 모바일에서 소개글이 body 전체 사용하도록 수정 (+ 모바일용 정적 배경 삽입)
- iOS Safari에서 z-index 적용 안되는 오류 해결 (-webkit-transform)

3/4
- 메인화면 배너 자동으로 넘어가게 수정
- 하단 nav에서 현재 선택된 동아리로 자동 스크롤되도록 수정
- 소개페이지 콘솔창에 출력되던 테스트 문구 제거
- 홈에 들어올 때마다 배너 넘어가는 타이머가 새로 추가되던 오류 수정

3/5
- 하단 nav에서 화면 밖에 있는 동아리로 스크롤할 때 화면 전체가 밀리던 버그 수정
- 지원하기 버튼 디자인 일부 수정
- 가입할 때 중복 계정 존재할 시 문의하기 링크로 로델라 문의 링크 뜨던 오류 수정

3/6
- 메인 페이지 디자인 일부 수정, 1차 결과 표시 칸 생성
- 지원서 목록(부원용)에서 기본값으로 취소한 지원서는 가림. 대신 '취소한 지원서도 보기' 링크를 맨 뒤에 달아둠.
- 1차 합격 추가, 메인 페이지에서 결과 확인 가능
- 1차 합격자 선택(부장용) 페이지 추가 및 관련 기능 추가
- 모든 지원서 내용 복사하기 페이지(부장용) 추가

3/7
- 1차 결과 문구 수정 (탈락 -> 불합격)
- 2차 면접 시간 등록 페이지(부장용) 추가
- 2차 면접 선택 페이지 활성화

3/8
- 메인페이지에 면접 관련 내용 추가, 면접 시간 맨 위로
- 면접시간 설정 페이지(부장용) 자동완성 오류 수정
- 면접시간 보기 페이지(부원용) 추가
