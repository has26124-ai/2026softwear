import streamlit as st
import time
import pandas as pd
from datetime import datetime

# --- 1. 페이지 기본 설정 ---
st.set_page_config(page_title="학생용 학습 타이머", page_icon="⏱️", layout="centered")

st.title("⏱️ 학생용 학습 타이머")
st.caption("과목을 선택하고 학습 시간을 기록해보세요!")

# --- 2. 세션 상태(Session State) 초기화 ---
# 앱이 리로드되어도 데이터가 유지되도록 초기값을 설정합니다.
if "elapsed_time" not in st.session_state:
    st.session_state.elapsed_time = 0  # 누적 초 단위 시간

if "is_running" not in st.session_state:
    st.session_state.is_running = False  # 타이머 작동 여부

if "records" not in st.session_state:
    st.session_state.records = []  # 과목별 학습 기록 리스트

# --- 3. 과목 선택 및 시간 표시 UI ---
subject = st.selectbox("📚 과목을 선택하세요", ["국어", "수학", "영어", "탐구", "기타"])

# 초 단위 시간을 "HH:MM:SS" 형식으로 변환하는 함수
def format_time(seconds):
    hrs = seconds // 3600
    mins = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hrs:02d}:{mins:02d}:{secs:02d}"

# 타이머 시계가 표시될 영역 생성
timer_placeholder = st.empty()

# --- 4. 제어 버튼 (시작, 일시정지, 초기화, 기록 저장) ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("▶️ 시작", use_container_width=True):
        st.session_state.is_running = True

with col2:
    if st.button("⏸️ 일시정지", use_container_width=True):
        st.session_state.is_running = False

with col3:
    if st.button("🔄 초기화", use_container_width=True):
        st.session_state.is_running = False
        st.session_state.elapsed_time = 0

with col4:
    if st.button("💾 기록 저장", use_container_width=True):
        if st.session_state.elapsed_time > 0:
            formatted_t = format_time(st.session_state.elapsed_time)
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 기록 저장
            st.session_state.records.append({
                "과목": subject,
                "학습 시간": formatted_t,
                "기록 일시": now_str
            })
            st.success(f"[{subject}] {formatted_t} 기록 완료!")
        else:
            st.warning("저장할 학습 시간이 없습니다.")

# --- 5. 타이머 루프 동작 처리 ---
# 타이머가 동작 중일 때 1초씩 누적하고 화면을 갱신합니다.
if st.session_state.is_running:
    timer_placeholder.markdown(f"<h1 style='text-align: center; color: #4CAF50;'>{format_time(st.session_state.elapsed_time)}</h1>", unsafe_allow_html=True)
    time.sleep(1)
    st.session_state.elapsed_time += 1
    st.rerun()
else:
    timer_placeholder.markdown(f"<h1 style='text-align: center; color: #888888;'>{format_time(st.session_state.elapsed_time)}</h1>", unsafe_allow_html=True)

# --- 6. 과목별 학습 기록 출력 ---
st.divider()
st.subheader("📊 학습 기록")

if st.session_state.records:
    df = pd.DataFrame(st.session_state.records)
    st.dataframe(df, use_container_width=True)
else:
    st.info("아직 저장된 학습 기록이 없습니다. 공부를 시작해보세요!")