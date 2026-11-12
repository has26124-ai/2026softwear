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
    st.caption("오늘 달성할 과목별 목표와 할 일 목록을 관리하세요.")

    # 할 일 목록 세션 상태 초기화
    if "todos" not in st.session_state:
        st.session_state.todos = []

    # 입력 폼
    with st.form("todo_form", clear_on_submit=True):
        col_subj, col_task = st.columns([1, 2])
        
        with col_subj:
            todo_subject = st.selectbox("과목", ["국어", "수학", "영어", "탐구", "기타"])
        
        with col_task:
            todo_task = st.text_input("할 일 입력", placeholder="예: 개념원리 30p~35p 풀기")
        
        submit_button = st.form_submit_button("➕ 할 일 추가", use_container_width=True)

        if submit_button:
            if todo_task.strip() != "":
                st.session_state.todos.append({
                    "subject": todo_subject,
                    "task": todo_task
                })
                st.success(f"'{todo_task}' 항목이 추가되었습니다!")
                st.rerun()
            else:
                st.warning("할 내용을 입력해 주세요.")

    st.divider()
    st.subheader("📌 할 일 목록")

    # 할 일 목록 출력 및 삭제 처리
    if st.session_state.todos:
        for idx, item in enumerate(st.session_state.todos):
            c1, c2 = st.columns([4, 1])
            with c1:
                st.write(f"**[{item['subject']}]** {item['task']}")
            with c2:
                if st.button("🗑️ 삭제", key=f"del_todo_{idx}", use_container_width=True):
                    st.session_state.todos.pop(idx)
                    st.rerun()
    else:
        st.info("등록된 할 일이 없습니다. 새로운 할 일을 추가해보세요!")

# 3-3. 공부회고 메뉴
elif menu == "✏️ 공부회고":
    st.title("✏️ 과목별 공부 회고")
    st.caption("오늘 공부하며 부족했던 부분과 반성할 점을 기록하고 다음 학습 계획에 반영해보세요.")

    # 회고 목록 세션 상태 초기화
    if "reflections" not in st.session_state:
        st.session_state.reflections = []

    # 회고 입력 폼
    with st.form("reflection_form", clear_on_submit=True):
        ref_subject = st.selectbox("📚 복습/회고할 과목", ["국어", "수학", "영어", "탐구", "기타"])
        
        good_point = st.text_area("👍 오늘 잘한 점 (칭찬할 부분)", placeholder="예: 집중력을 잃지 않고 타이머 시간 동안 끝까지 문제집을 풀었다.")
        bad_point = st.text_area("💡 부족했던 부분 & 반성할 점", placeholder="예: 수학 3단원 공식 암기가 부족해서 오답이 많았다. 내일은 개념 복습부터 해야겠다.")
        
        submit_ref = st.form_submit_button("📝 회고 저장하기", use_container_width=True)

        if submit_ref:
            if good_point.strip() != "" or bad_point.strip() != "":
                now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
                st.session_state.reflections.append({
                    "subject": ref_subject,
                    "good": good_point if good_point.strip() else "작성 없음",
                    "bad": bad_point if bad_point.strip() else "작성 없음",
                    "date": now_str
                })
                st.success(f"[{ref_subject}] 공부 회고가 저장되었습니다!")
                st.rerun()
            else:
                st.warning("잘한 점이나 부족했던 점 중 최소 하나 이상을 작성해 주세요.")

    st.divider()
    st.subheader("📜 작성한 회고 목록")

    # 저장된 회고 목록 출력
    if st.session_state.reflections:
        for idx, ref in enumerate(reversed(st.session_state.reflections)):
            # reversed를 사용하여 최근 작성된 회고가 상단에 오도록 설정
            actual_idx = len(st.session_state.reflections) - 1 - idx
            
            with st.expander(f"📌 [{ref['subject']}] 회고 - {ref['date']}"):
                st.markdown(f"**👍 잘한 점:**\n{ref['good']}")
                st.markdown(f"**💡 부족했던 점 & 반성:**\n{ref['bad']}")
                
                if st.button("🗑️ 회고 삭제", key=f"del_ref_{actual_idx}"):
                    st.session_state.reflections.pop(actual_idx)
                    st.rerun()
    else:
        st.info("아직 작성된 공부 회고가 없습니다. 오늘 학습을 돌아보고 첫 회고를 남겨보세요!")
