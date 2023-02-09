# https://forms.gle/ro1Mo6yds7CSHiM19

form_data = {
  "title": "한국어 예시 설문지",
  "description": "이건 설명이에요! / Extform by HURDOO",
  "items": [
    {
      "title": "섹션 제목",
      "helpText": "설명",
      "id": 1198406534,
      "type": "SECTION_HEADER",
      "extra": {}
    },
    {
      "title": "객관식 질문",
      "helpText": "",
      "id": 984420844,
      "type": "MULTIPLE_CHOICE",
      "extra": {
        "choices": [
          {
            "value": "옵션 1"
          },
          {
            "value": "옵션 2"
          },
          {
            "value": "옵션 3"
          }
        ],
        "hasOtherOption": True,
        "required": True
      }
    },
    {
      "title": "체크박스",
      "helpText": "",
      "id": 527425354,
      "type": "CHECKBOX",
      "extra": {
        "choices": [
          {
            "value": "옵션 1"
          },
          {
            "value": "옵션 2"
          },
          {
            "value": "옵션 3"
          }
        ],
        "hasOtherOption": True,
        "required": False
      }
    },
    {
      "title": "드롭다운",
      "helpText": "이건 설명이에오",
      "id": 1754718226,
      "type": "LIST",
      "extra": {
        "choices": [
          {
            "value": "옵션 1"
          },
          {
            "value": "옵션 2"
          },
          {
            "value": "옵션 3"
          }
        ],
        "required": True
      }
    },
    {
      "title": "단답형",
      "helpText": "",
      "id": 2042360110,
      "type": "TEXT",
      "extra": {
        "required": True
      }
    },
    {
      "title": "장문형 (5글자 이상)",
      "helpText": "",
      "id": 40010923,
      "type": "PARAGRAPH_TEXT",
      "extra": {
        "required": True
      }
    },
    {
      "title": "선형 배율",
      "helpText": "",
      "id": 1729172976,
      "type": "SCALE",
      "extra": {
        "leftLabel": "맨 왼쪽엔 이렇게 들어가유",
        "rightLabel": "최대",
        "lowerBound": 1,
        "upperBound": 5,
        "required": True
      }
    },
    {
      "title": "객관식 그리드 (1열 중복 불가)",
      "helpText": "",
      "id": 1747983985,
      "type": "GRID",
      "extra": {
        "rows": [
          "행1",
          "행 2",
          "행 3"
        ],
        "columns": [
          "1 열",
          "열 2",
          "열 3",
          "열 4"
        ],
        "required": True
      }
    },
    {
      "title": "체크박스 그리드 (행마다 필수응답 아님)",
      "helpText": "",
      "id": 1505186486,
      "type": "CHECKBOX_GRID",
      "extra": {
        "rows": [
          "행1",
          "행 2",
          "행 3",
          "행 4"
        ],
        "columns": [
          "1 열",
          "열 2",
          "열 3"
        ],
        "required": False
      }
    },
    {
      "title": "날짜 (연도 포함)",
      "helpText": "",
      "id": 1863290637,
      "type": "DATE",
      "extra": {
        "includesYear": True,
        "required": True
      }
    },
    {
      "title": "날짜 (시간 포함)",
      "helpText": "",
      "id": 1912205331,
      "type": "DATETIME",
      "extra": {
        "includesYear": True,
        "required": True
      }
    },
    {
      "title": "시간",
      "helpText": "",
      "id": 1172953185,
      "type": "TIME",
      "extra": {
        "required": True
      }
    },
    {
      "title": "시간 (기간)",
      "helpText": "",
      "id": 1268965762,
      "type": "DURATION",
      "extra": {
        "required": True
      }
    },

    {
      "title": "이미지",
      "helpText": "",
      "id": 1845279172,
      "type": "IMAGE",
      "extra": {
        "image": "###",
        "imageType": "image/png",
        "alignment": "LEFT"
      }
    }
  ],
  "token": "2f40bdf9-04cf-41a0-bbd5-96a513dc1b8a"
}