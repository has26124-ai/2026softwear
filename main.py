import streamlit as st
import time
import pandas as pd
from datetime import datetime

# --- 1. 페이지 기본 설정 ---
st.set_page_config(page_title="학생용 학습 및 관리 앱", page_icon="📝", layout="centered")

# --- 2. 사이드바 메뉴 생성 ---
st.sidebar.title("📌 메뉴")
menu = st.sidebar.radio(
    "원하는 기능을 선택하세요:",
    ["⏱️ 공부타이머", "📋 오늘 할일", "✏️ 공부회고"]
)

# --- 3. 메뉴별 화면 구성 ---

# 3-1. 공부타이머 메뉴
if menu == "⏱️ 공부타이머":
    st.title("⏱️ 학생용 학습 타이머")
    st.caption("과목을 선택하고 학습 시간을 기록해보세요!")

    # 세션 상태(Session State) 초기화
    if "elapsed_time" not in st.session_state:
        st.session_state.elapsed_time = 0  # 누적 초 단위 시간

    if "is_running" not in st.session_state:
        st.session_state.is_running = False  # 타이머 작동 여부

    if "records" not in st.session_state:
        st.session_state.records = []  # 과목별 학습 기록 리스트

    # 과목 선택
    subject = st.selectbox("📚 과목을 선택하세요", ["국어", "수학", "영어", "탐구", "기타"])

    # 초 단위 시간을 "HH:MM:SS" 형식으로 변환하는 함수
    def format_time(seconds):
        hrs = seconds // 3600
        mins = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hrs:02d}:{mins:02d}:{secs:02d}"

    # 타이머 시계 표시 영역
    timer_placeholder = st.empty()

    # 제어 버튼 (시작, 일시정지, 초기화, 기록 저장)
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

    # 타이머 루프 동작 처리
    if st.session_state.is_running:
        timer_placeholder.markdown(f"<h1 style='text-align: center; color: #4CAF50;'>{format_time(st.session_state.elapsed_time)}</h1>", unsafe_allow_html=True)
        time.sleep(1)
        st.session_state.elapsed_time += 1
        st.rerun()
    else:
        timer_placeholder.markdown(f"<h1 style='text-align: center; color: #888888;'>{format_time(st.session_state.elapsed_time)}</h1>", unsafe_allow_html=True)

    # 과목별 학습 기록 출력
    st.divider()
    st.subheader("📊 학습 기록")

    if st.session_state.records:
        df = pd.DataFrame(st.session_state.records)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("아직 저장된 학습 기록이 없습니다. 공부를 시작해보세요!")

# 3-2. 오늘 할일 메뉴
elif menu == "📋 오늘 할일":
    st.title("📋 오늘 할일")
    st.caption("오늘 달성할 목표와 할 일 목록을 관리하세요.")

# 3-3. 공부회고 메뉴
elif menu == "✏️ 공부회고":
    st.title("✏️ 공부회고")
    st.caption("오늘 하루의 학습 과정을 돌아보고 회고를 작성하세요.")