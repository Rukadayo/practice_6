import streamlit as st
import pandas as pd
import datetime

st.title("📝 간단 설문조사서")
st.write("아래 설문에 응답해주세요.")

# st.form을 사용하여 입력 필드를 하나의 폼으로 묶습니다.
with st.form("survey_form"):
    st.header("1. 기본 인적사항")
    
    # 이름 (텍스트 입력)
    name = st.text_input("이름")
    
    # 나이 (슬라이더) - 요청하신 슬라이더를 사용합니다.
    age = st.slider("나이", min_value=10, max_value=100, value=25)
    
    st.write("---")
    
    st.header("2. 소속 정보")
    
    # 소속 (두 개의 열로 나누어 배치)
    col1, col2 = st.columns(2)
    with col1:
        school = st.text_input("학교")
        student_id = st.text_input("학번 (예: 24학번)")
    with col2:
        major = st.text_input("학과")

    st.write("---")

    st.header("3. 관심사")
    
    # 취미 (다중 선택)
    hobbies = st.multiselect(
        "취미를 모두 선택해주세요 (여러 개 선택 가능)",
        ["운동", "독서", "영화 감상", "음악 감상", "게임", "여행", "코딩"]
    )
    
    # '제출하기' 버튼
    # 이 버튼을 눌렀을 때만 form 안의 데이터가 전송됩니다.
    submitted = st.form_submit_button("제출하기")

# '제출하기' 버튼이 눌렸을 때 실행될 코드
if submitted:
    if not name:
        st.warning("이름을 입력해주세요!")
    else:
        st.success("🎉 설문조사 제출이 완료되었습니다!")
        
        st.header("📋 제출된 응답")
        
        # 제출된 데이터를 딕셔너리로 만듭니다.
        response_data = {
            "항목": ["이름", "나이", "학교", "학과", "학번", "취미"],
            "응답": [name, age, school, major, student_id, ", ".join(hobbies) if hobbies else "선택 안 함"]
        }
        
        # Pandas DataFrame으로 변환하여 표로 예쁘게 보여줍니다.
        df = pd.DataFrame(response_data)
        st.table(df)
        
        st.info(f"설문제출시간: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
