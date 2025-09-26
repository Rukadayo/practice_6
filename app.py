import streamlit as st
import pandas as pd
import datetime

st.title("📝 간단 설문조사서 (관리자 기능 추가)")

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
        # 현재 응답 데이터를 딕셔너리로 저장
        new_response = {
            "제출시간": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "이름": name,
            "나이": age,
            "학교": school,
            "학과": major,
            "학번": student_id,
            "취미": ", ".join(hobbies) if hobbies else "선택 안 함"
        }
        
        # 전체 응답 리스트에 현재 응답 추가
        st.session_state.all_responses.append(new_response)
        st.success("🎉 설문조사 제출이 완료되었습니다! 감사합니다.")

# --- 2. 관리자 확인 기능 (사이드바) ---
st.sidebar.title("👨‍💼 관리자 모드")
password = st.sidebar.text_input("비밀번호를 입력하세요:", type="password")

# 간단한 비밀번호 확인 로직 (실제 사용 시에는 더 안전한 방법 사용 권장)
if password == "0501":
    st.sidebar.success("인증되었습니다.")
    
    st.write("---")
    st.header("📊 전체 제출 데이터 확인")

    if st.session_state.all_responses:
        # 전체 응답 데이터를 DataFrame으로 변환
        all_df = pd.DataFrame(st.session_state.all_responses)
        st.dataframe(all_df)
        
        # CSV 다운로드 버튼
        # DataFrame을 CSV 형식의 문자열로 변환
        csv = all_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="CSV 파일로 다운로드",
            data=csv,
            file_name="survey_responses.csv",
            mime="text/csv",
        )
    else:
        st.warning("아직 제출된 데이터가 없습니다.")

elif password:
    st.sidebar.error("비밀번호가 틀렸습니다.")