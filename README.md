다음뉴스 키워드 및 언론사 기반 기사 크롤링
=======

1. 언론사 및 키워드 설정
    1. [다음 뉴스검색창](https://search.daum.net/search?nil_suggest=btn&w=news&cluster=y&q=%EB%8B%A4%EC%9D%8C&cpname=%EC%97%B0%ED%95%A9%EB%89%B4%EC%8A%A4&cp=16X5Xh1MWS7Qt1sMrW) 에서 `언론사전체 ˅` 버튼을 클릭하여 `언론사 직접입력`을 누르고 원하는 언론사를 입력
    2. URL에서 `cp=` 다음의 값을 복사하여 `src/env.py`에 저장
       - https://search.daum.net/search?nil_suggest=btn&w=news&cluster=y&q=%EB%8B%A4%EC%9D%8C&cpname=%EC%97%B0%ED%95%A9%EB%89%B4%EC%8A%A4&cp= **`16X5Xh1MWS7Qt1sMrW`**
    3. 원하는 키워드를 `src/env.py`의 `KEYWORD`로 설정
    4. `DATE_RANGE` 상수에 검색기간 입력 (`YYYYMMDD` 형태, # 검색기간 시작일 0시 0분 0초부터 종료일 11시 59분 59초까지 검색됨)
2. 크롤링 시작
    ```
    python src/data/crawl.py
    ```
3. `data/raw/{언론사이름}` 폴더에 각 기간별로 크롤링된 기사 파일 확인


Topic Modeling Articles on UBI 
==============================
This project aims to analyze how major South Korea media's sentiment has shifted since cash relief for the COVID-19 pandemic were given out nationwide. 

1. Scrape articles containing certain keywords on [Daum News](https://news.daum.net).
2. Prep the corpus: text cleaning, tokenization, etc.
3. Run NMF and LDA to gauge distribution of topics
4. Based on 3, label a sample of the articles. (done manually, outside this project--TODO: share data and labelling standards)
5. Learn a sentiment classification model from 4 (done in [ubi_article_sentiment](https://github.com/suzinyou/ubi_article_sentiment))

Project Organization
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- Crawled articles 크롤링된 기사 (언론사별로 폴더 생성)
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    └── src                <- Source code for use in this project.
        ├── __init__.py    <- Makes src a Python module
        │
        ├── data           <- Scripts to download or generate data
        │   └── make_dataset.py
        │
        ├── features       <- Scripts to turn raw data into features for modeling
        │   └── build_features.py
        │
        ├── models         <- Scripts to train models and then use trained models to make
        │   │                 predictions
        │   ├── predict_model.py
        │   └── train_model.py
        │
        └── visualization  <- Scripts to create exploratory and results oriented visualizations
            └── visualize.py
    


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
