import streamlit as st
import pandas as pd
import datetime

st.title("📝 간단 설문조사서 (관리자 기능 강화)")

# session_state에 'all_responses' 리스트가 없으면 초기화
if 'all_responses' not in st.session_state:
    st.session_state.all_responses = []

# --- 1. 설문조사 입력 폼 ---
with st.form("survey_form"):
    st.header("1. 기본 인적사항")
    name = st.text_input("이름")
    age = st.slider("나이", min_value=10, max_value=100, value=25)
    
    st.header("2. 소속 정보")
    col1, col2 = st.columns(2)
    with col1:
        school = st.text_input("학교")
        student_id = st.text_input("학번 (예: 24학번)")
    with col2:
        major = st.text_input("학과")

    st.header("3. 관심사")
    hobbies = st.multiselect(
        "취미를 모두 선택해주세요 (여러 개 선택 가능)",
        ["운동", "독서", "영화 감상", "음악 감상", "게임", "여행", "코딩"]
    )
    
    submitted = st.form_submit_button("제출하기")

# '제출하기' 버튼이 눌렸을 때 실행될 코드
if submitted:
    if not name:
        st.warning("이름을 입력해주세요!")
    else:
        new_response = {
            "제출시간": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "이름": name,
            "나이": age,
            "학교": school,
            "학과": major,
            "학번": student_id,
            "취미": ", ".join(hobbies) if hobbies else "선택 안 함"
        }
        st.session_state.all_responses.append(new_response)
        st.success("🎉 설문조사 제출이 완료되었습니다! 감사합니다.")

# --- 2. 관리자 확인 기능 (사이드바) ---
st.sidebar.title("👨‍💼 관리자 모드")
password = st.sidebar.text_input("비밀번호를 입력하세요:", type="password")

if password == "0501":
    st.sidebar.success("인증되었습니다.")
    
    st.write("---")
    st.header("📊 전체 제출 데이터 관리")

    if st.session_state.all_responses:
        # 삭제할 응답의 인덱스를 저장할 리스트
        indices_to_delete = []
        
        # 전체 응답을 순회하며 화면에 표시
        for i, response in enumerate(st.session_state.all_responses):
            st.subheader(f"응답 {i+1} (제출자: {response['이름']})")
            st.table(pd.DataFrame(response.items(), columns=["항목", "응답"]))
            
            # 삭제 버튼을 누르면 해당 인덱스를 리스트에 추가
            if st.button(f"응답 {i+1} 삭제하기", key=f"delete_{i}"):
                indices_to_delete.append(i)

        # 삭제할 인덱스가 있으면, 역순으로 정렬하여 삭제 실행
        if indices_to_delete:
            for i in sorted(indices_to_delete, reverse=True):
                st.session_state.all_responses.pop(i)
            st.rerun()

        st.write("---")
        # CSV 다운로드 버튼 (남아있는 데이터를 기준으로 생성)
        if st.session_state.all_responses:
            all_df = pd.DataFrame(st.session_state.all_responses)
            csv = all_df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="남은 데이터 전체 CSV로 다운로드",
                data=csv,
                file_name="survey_responses.csv",
                mime="text/csv",
            )
    else:
        st.warning("아직 제출된 데이터가 없습니다.")

elif password:
    st.sidebar.error("비밀번호가 틀렸습니다.")
