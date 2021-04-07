from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]

KEYWORD = '"기본소득"'
HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

CP_DICT = {  # 다음 뉴스의 언론 코드
    '조선일보': '16d4PV266g2j-N3GYq',
    '한겨레': '16nzyJHdH5ORpabfqG',
    '경향신문': '16akMkKFDu6n8GTzZr',
    '동아일보': '16bOiOx4gG2S18EPLj',
}

DATE_RANGES = [
    ('20170101', '20200731'), 
    ('20210101', '20210201')
]  # 시작과 끝 기간, 한 기간, 한 언론사마다 한 파일 생성 