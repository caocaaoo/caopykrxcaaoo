# caopykrxcaaoo
주식 시장에서 저평가된 종목을 추리는 파이썬 스크립트입니다.
pykrx 라이브러리를 사용하여 주식 시장 데이터를 수집하고, pandas를 활용하여 데이터를 추려냈습니다.
여러 기술적, 펀더멘탈 지표들을 종합하여 각 종목에 대한 종합 점수를 산출하고 이를 기반으로 매수할만한 저평가 종목을 추려냅니다.



사용된 라이브러리 및 도구
pykrx: 주식 시장 데이터를 실시간으로 불러오는 라이브러리 (https://github.com/sharebook-kr/pykrx)
pandas: 데이터 분석 및 조작을 위한 라이브러리
numpy: 수치 계산을 위한 라이브러리
VSCode: 코드 작성 및 실행을 위한 IDE



기능 및 작동 방법

1. 데이터 수집
pykrx 라이브러리를 이용해 주식 종목별 기본 정보, 거래량, 등락률, 펀더멘탈 지표 등의 데이터를 수집합니다.
2. 데이터 전처리
수집한 데이터를 pandas DataFrame 형태로 변환하여 조작하기 쉽게 만듭니다.
필요한 계산 및 변환을 통해 새로운 지표들을 도출합니다 (예: 내재가치, SMA20 등).
3. 점수 산출
각 종목에 대해 여러 지표들을 기반으로 점수를 산출합니다.
산출된 점수를 기반으로 종목들을 정렬하고 상위 종목들을 선택합니다.
4. 필터링
특정 조건 (예: PBR < 3.5, PER <= 평균 PER) 을 만족하는 종목만을 최종적으로 선택합니다.
5. 결과 출력
최종적으로 선택된 종목들의 리스트를 출력합니다, 여기에는 종목 코드, 종목명, 점수, 펀더멘탈 지표들이 포함됩니다.



개선 및 활용 방안

추가적인 지표나 알고리즘을 도입하여 점수 산출 방법을 개선할 수 있습니다.
이 코드를 기반으로 주기적인 리밸런싱, 포트폴리오 구성 등의 투자 전략을 구현할 수 있습니다.
다양한 시각화 도구를 활용하여 분석 결과를 더 직관적으로 확인할 수 있습니다.
