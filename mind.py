import streamlit as st
import pandas as pd
import os
import datetime

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
        new_entry = {"날짜": str(date), "감정": emotion, "내용": entry}
        # DataFrame에 새로운 일기 추가
        diary_df = pd.concat([diary_df, pd.DataFrame([new_entry])], ignore_index=True)
        diary_df.to_csv(DIARY_FILE, index=False)  # 업데이트된 데이터를 CSV에 저장
        st.success("일기가 추가되었습니다!")
    else:
        st.error("일기 내용을 입력해주세요.")

# 작성된 일기 목록 표시
if not diary_df.empty:
    st.subheader("작성된 일기 목록")

    # 감정 선택 필터
    filter_emotion = st.selectbox("감정으로 필터링", ["전체"] + diary_df['감정'].unique().tolist())

    if filter_emotion == "전체":
        filtered_df = diary_df
    else:
        filtered_df = diary_df[diary_df['감정'] == filter_emotion]

    # 일기 검색 기능
    search_keyword = st.text_input("키워드로 검색", "")
    if search_keyword:
        filtered_df = filtered_df[filtered_df['내용'].str.contains(search_keyword, na=False)]

    for i in range(len(filtered_df)):
        st.write(f"**날짜**: {filtered_df.iloc[i]['날짜']} | **감정**: {filtered_df.iloc[i]['감정']}")
        st.write(f"**내용**: {filtered_df.iloc[i]['내용']}")
        st.write("---")  # 구분선
else:
    st.write("아직 작성된 일기가 없습니다.")

# ---- 사이드바에 정신 건강 테스트 추가 ----
st.sidebar.header("정신 건강 테스트")

# 질문 리스트 (질문 수 늘리기)
questions = [
    "최근 몇 주간 기분이 우울했다고 느끼나요?",
    "사라지지 않는 불안이나 긴장을 느끼나요?",
    "일상 활동에 대한 흥미를 잃으셨나요?",
    "최근에 수면에 문제가 있나요? (예: 불면증, 과다수면)",
    "자신에 대한 부정적인 생각이 자주 드시나요?",
    "사람들과의 관계에 문제가 있나요?",
    "자주 피로감을 느끼거나 에너지가 부족하다고 느끼나요?",
    "어떤 일이나 사람에게 과도하게 화가 나거나 실망하셨나요?",
    "최근에 중요한 결정을 잘 내리지 못하고 있나요?",
    "자신의 감정을 잘 표현하지 못하고 있나요?",
]

# 각 질문에 대한 점수 초기화
scores = []

# 질문 안에 응답 받기
for question in questions:
    answer = st.sidebar.radio(question, ["전혀 그렇지 않다", "가끔 그렇다", "자주 그렇다", "항상 그렇다"], key=question)
    scores.append(answer)

# 테스트 결과 버튼
if st.sidebar.button("결과 확인"):
    total_score = 0
    scoring_map = {"전혀 그렇지 않다": 0, "가끔 그렇다": 1, "자주 그렇다": 2, "항상 그렇다": 3}

    for score in scores:
        total_score += scoring_map[score]

    # 결과에 대한 설명
    if total_score <= 5:
        result = "정신 건강이 안정적인 상태입니다. 좋은 감정 관리법을 유지하세요."
        advice = "꾸준한 운동과 적절한 수면, 균형 잡힌 식사를 통해 건강을 유지하세요.\n스스로의 감정을 표현하는 일기를 지속적으로 작성해 보세요."
    elif total_score <= 10:
        result = "일부 우울감이나 불안이 있을 수 있습니다. 필요할 경우 지원을 요청하세요."
        advice = "일상에서 작은 목표를 설정하고 달성해보세요. 친구나 가족과 대화하여 감정을 나누는 것도 도움이 될 수 있습니다.\n전문가와 상담하는 것도 고려해보세요."
    else:
        result = "심리적인 어려움이 있을 수 있습니다. 전문가와 상담하는 것이 좋습니다."
        advice = "전문가의 도움을 받는 것이 중요합니다. 자신의 상황을 이야기하고 적절한 도움과 지원을 받으세요.\n신뢰할 수 있는 친구나 가족과 상담하는 것도 좋은 방법입니다."

    st.sidebar.success(f"당신의 점수는 {total_score}점입니다. {result}")
    st.sidebar.text(f"권장 사항: {advice}")

# 정신 건강 관련 퀴즈 게임 추가
st.subheader("정신 건강 퀴즈 게임")

quiz_questions = {
    "정신 건강은 무엇인가요?": ["신체적인 건강 상태", "정신적, 정서적 그리고 사회적 복지", "경제적 안정"],
    "정신 건강 문제는 어떻게 예방할 수 있나요?": ["규칙적인 운동", "건강한 식습관", "모든 선택이 다 정답이다"],
    "스트레스를 해소하는 방법은?": ["명상과 심호흡", "무시하기", "과음하기"],
    "정신 건강 전문가의 도움이 필요한 징후는 무엇인가요?": ["기분이 좋을 때", "감정 조절이 힘든 경우", "친구와 자주 노는 경우"],
    "어떤 생활 습관이 정신 건강에 긍정적인 영향을 미칠 수 있을까요?": ["규칙적인 수면", "정크푸드 섭취", "혼자 있는 시간 늘리기"],
    "어떤 상황에서 스트레스를 받을 수 있나요?": ["과도한 업무", "충분한 휴식", "자주 운동하는 것"],
    "긍정적인 마인드셋을 유지하기 위한 방법은 무엇인가요?": ["감사 일기 쓰기", "좋은 느낌을 무시하기", "나쁜 생각을 계속하기"],
    "우울증의 일반적인 증상은 무엇인가요?": ["우울감과 잃어버린 흥미", "과도한 즐거움", "불면증 없이 잘 자는 것"],
    "스트레스를 줄이기 위한 간단한 기술은 무엇인가요?": ["적극적인 친구에게 이야기하기", "혼자 방에 틀어박히기", "SNS에서 더 많이 활동하기"],
    "정신 건강을 지키기 위해 규칙적으로 무엇을 해야 할까요?": ["전문 상담받기", "감정 억누르기", "모든 문제를 스스로 해결하기"],
}

score = 0

# 퀴즈 질문에 대한 답변 받기
for question, options in quiz_questions.items():
    answer = st.radio(question, options, key=question)
    if answer == options[1]:  # 두 번째 옵션이 정답
        score += 1

# 퀴즈 결과 확인 버튼
if st.button("퀴즈 결과 확인"):
    st.success(f"퀴즈 점수는 {score}/{len(quiz_questions)}입니다!")
    if score == len(quiz_questions):
        st.balloons()
        st.text("훌륭합니다! 정신 건강에 대한 이해도가 높습니다.")
    elif score > 0:
        st.text("좋습니다! 계속해서 배우고 이해해 나가세요.")
    else:
        st.text("정신 건강에 대한 추가적인 학습이 필요합니다. 관련 정보를 찾아보세요.")
