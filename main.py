import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh
import time

# --- 페이지 기본 설정 ---
st.set_page_config(page_title="학생용 학습 타이머", page_icon="⏱️", layout="centered")

st.title("⏱️ 학생용 과목별 학습 타이머")
st.write("오늘의 공부 목표를 달성해 보세요! 과목을 선택하고 타이머를 시작하세요.")

# --- Session State (상태 저장) 초기화 ---
if "elapsed_time" not in st.session_state:
    st.session_state.elapsed_time = 0  # 현재 측정 중인 시간 (초)
if "is_running" not in st.session_state:
    st.session_state.is_running = False  # 타이머 작동 여부
if "last_start_time" not in st.session_state:
    st.session_state.last_start_time = None  # 마지막 시작 시각
if "subjects" not in st.session_state:
    st.session_state.subjects = ["국어", "수학", "영어", "탐구"]  # 기본 과목 목록
if "records" not in st.session_state:
    # 과목별 누적 공부 시간 (초 단위)
    st.session_state.records = {subject: 0 for subject in st.session_state.subjects}

# --- 1초마다 자동 갱신 (타이머가 실행 중일 때만 동작) ---
if st.session_state.is_running:
    st_autorefresh(interval=1000, key="timer_refresh")
    st.session_state.elapsed_time += 1

# --- 초 단위 시간을 보기 좋은 형식(HH:MM:SS)으로 변환하는 함수 ---
def format_time(seconds):
    hrs = seconds // 3600
    mins = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hrs:02d}:{mins:02d}:{secs:02d}"

# --- 사이드바: 과목 관리 ---
st.sidebar.header("📚 과목 설정")
new_subject = st.sidebar.text_input("새 과목 추가")
if st.sidebar.button("과목 추가"):
    if new_subject and new_subject not in st.session_state.subjects:
        st.session_state.subjects.append(new_subject)
        st.session_state.records[new_subject] = 0
        st.sidebar.success(f"'{new_subject}' 과목이 추가되었습니다!")
    elif new_subject in st.session_state.subjects:
        st.sidebar.warning("이미 존재하는 과목입니다.")

selected_subject = st.selectbox("공부할 과목을 선택하세요", st.session_state.subjects)

# --- 메인 화면: 타이머 디스플레이 및 버튼 ---
st.markdown("---")
st.subheader(f"📖 현재 선택된 과목: [{selected_subject}]")

# 타이머 시계 표시 (큰 글씨)
st.markdown(
    f"<h1 style='text-align: center; font-size: 80px; color: #4CAF50;'>{format_time(st.session_state.elapsed_time)}</h1>",
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("▶️ 시작", use_container_width=True):
        st.session_state.is_running = True

with col2:
    if st.button("⏸️ 일시정지", use_container_width=True):
        st.session_state.is_running = False

with col3:
    if st.button("⏹️ 기록 및 초기화", use_container_width=True):
        st.session_state.is_running = False
        # 현재 측정된 시간을 해당 과목에 누적
        st.session_state.records[selected_subject] += st.session_state.elapsed_time
        st.success(f"{selected_subject} 과목에 {format_time(st.session_state.elapsed_time)} 저장이 완료되었습니다!")
        st.session_state.elapsed_time = 0

st.markdown("---")

# --- 과목별 학습 기록 및 통계 ---
st.subheader("📊 과목별 공부 시간 기록")

# 데이터를 데이터프레임으로 변환하여 시각화
record_data = []
for subj, sec in st.session_state.records.items():
    record_data.append({
        "과목": subj,
        "공부 시간": format_time(sec),
        "총 시간(분)": round(sec / 60, 1)
    })

df = pd.DataFrame(record_data)

# 표 및 차트 출력
st.table(df[["과목", "공부 시간"]])

# 차트 표시 (공부한 시간이 1초라도 있을 때만)
if sum(st.session_state.records.values()) > 0:
    st.bar_chart(df.set_index("과목")["총 시간(분)"])
