import streamlit as st
import pandas as pd
import os
import datetime

# matplotlib 라이브러리가 설치되어 있는지 확인하고 import 해오기
try:
    import matplotlib.pyplot as plt
except ImportError:
    st.error("matplotlib를 설치해야 합니다. `pip install matplotlib`를 실행하여 설치해 주세요.")
    st.stop()  # ImportError가 발생하면 앱 실행 중단

# 나머지 코드...
# CSV 파일 경로
DIARY_FILE = 'diary_entries.csv'

# 기존 일기 데이터 로드
if os.path.exists(DIARY_FILE):
    diary_df = pd.read_csv(DIARY_FILE)
else:
    diary_df = pd.DataFrame(columns=["날짜", "감정", "내용"])

# 감정 점수 맵
emotion_scores = {
    "기쁨": 3,
    "평화": 2,
    "혼란": 1,
    "불안": -1,
    "분노": -2,
    "슬픔": -3,
    "기타": 0
}

# 앱의 제목
st.title("감정 일기 및 정신 건강 테스트")

# 감정 선택
emotion = st.selectbox("오늘의 감정은 무엇인가요?", list(emotion_scores.keys()))

# 날짜 선택
date = st.date_input("날짜 선택", datetime.datetime.today())

# 일기 입력 필드
entry = st.text_area("오늘의 생각과 감정 기록하기")

# 일기 추가 버튼
if st.button("일기 추가"):
    if entry:
        new_entry = {"날짜": str(date), "감정": emotion}
        # DataFrame에 새로운 일기 추가
        diary_df = pd.concat([diary_df, pd.DataFrame([new_entry])], ignore_index=True)
        diary_df.to_csv(DIARY_FILE, index=False)  # 업데이트된 데이터를 CSV에 저장
        st.success("일기가 추가되었습니다!")
    else:
        st.error("일기 내용을 입력해주세요.")

# 감정 분석 시각화
if not diary_df.empty:
    st.subheader("감정 분석")

    # 감정 점수 계산
    diary_df["감정 점수"] = diary_df["감정"].map(emotion_scores)
    diary_df["날짜"] = pd.to_datetime(diary_df["날짜"])

    # 날짜별 감정 평균 계산
    daily_avg = diary_df.groupby("날짜")["감정 점수"].mean().reset_index()

    # 그래프 표시
    plt.figure(figsize=(10, 5))
    plt.plot(daily_avg["날짜"], daily_avg["감정 점수"], marker='o')
    plt.title("일기 작성 날짜별 평균 감정 점수")
    plt.xlabel("날짜")
    plt.ylabel("평균 감정 점수")
    plt.axhline(0, color='red', linestyle='--', label='중립 점수')
    plt.legend()
    st.pyplot(plt)

# 나머지 코드...
