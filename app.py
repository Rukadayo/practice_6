import streamlit as st
import pandas as pd
import datetime
import openai
import os
from dotenv import load_dotenv # .env 파일을 읽어오기 위한 라이브러리

# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()

# os.getenv()를 사용해 .env 파일에 저장된 API 키를 안전하게 불러옵니다.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# --- AI 요약 함수 (OpenAI 버전) ---
def get_ai_summary(responses_df):
    """OpenAI API를 호출하여 데이터 요약을 요청하는 함수"""
    
    # 데이터프레임을 AI가 이해하기 쉬운 문자열로 변환
    data_string = responses_df.to_string()
    
    # AI에게 보낼 프롬프트 (요청사항)
    prompt = f"""
    다음은 설문조사 응답 데이터입니다.
    
    {data_string}
    
    이 데이터를 바탕으로 아래 항목에 대해 한국어로 인사이트를 요약해 주세요:
    1. 전체 응답자 수
    2. 응답자들의 평균 나이와 나이 분포 특징
    3. 가장 많이 참여한 학과나 학교
    4. 가장 인기 있는 취미
    5. 프로그래밍에 대한 전반적인 만족도 경향
    6. 응답자들이 주로 어떤 졸업 후 계획을 가지고 있는지
    7. 전체적인 내용을 종합하여 자유롭게 분석 코멘트
    """
    
    try:
        # OpenAI 클라이언트 초기화 (위에서 불러온 OPENAI_API_KEY 변수 사용)
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
        # ChatCompletion API 호출
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 설문조사 데이터를 분석하고 요약해주는 유용한 AI 어시스턴트입니다."},
                {"role": "user", "content": prompt}
            ]
        )
        summary = response.choices[0].message.content
        return summary
    except Exception as e:
        if not OPENAI_API_KEY:
            return "OpenAI API 키가 .env 파일에 설정되지 않았거나 파일을 불러오지 못했습니다. .env 파일을 확인해주세요."
        return f"OpenAI 요약 생성 중 오류가 발생했습니다: {e}\nAPI 키가 올바른지 확인해주세요."

# --- 앱 UI 구성 ---
st.title("📝 간단 설문조사서 (AI 기능 탑재)")

if 'all_responses' not in st.session_state:
    st.session_state.all_responses = []

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
        "취미를 모두 선택해주세요",
        ["운동", "독서", "영화 감상", "음악 감상", "게임", "여행", "코딩"]
    )
    
    # --- 추가된 설문 항목 ---
    st.header("4. 추가 설문")
    grade = st.radio("학년을 선택하세요:", ["1학년", "2학년", "3학년", "4학년", "기타"])
    satisfaction = st.select_slider(
        "프로그래밍에 대한 전반적인 만족도는?",
        options=["매우 불만족", "불만족", "보통", "만족", "매우 만족"],
        value="보통"
    )
    post_grad_plan = st.selectbox(
        "졸업 후 계획은 무엇인가요?",
        ("취업", "대학원 진학", "창업", "해외 유학", "미정")
    )
    languages = st.multiselect(
        "주로 사용하는 프로그래밍 언어는? (다중 선택 가능)",
        ["Python", "JavaScript", "Java", "C/C++", "SQL", "R", "Kotlin/Swift"]
    )
    comment = st.text_area("자유롭게 의견을 남겨주세요.")
    
    submitted = st.form_submit_button("제출하기")

if submitted:
    if not name:
        st.warning("이름을 입력해주세요!")
    else:
        new_response = {
            "제출시간": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "이름": name, "나이": age, "학교": school, "학과": major, "학번": student_id,
            "취미": ", ".join(hobbies) if hobbies else "선택 안 함",
            "학년": grade, "만족도": satisfaction, "졸업후계획": post_grad_plan,
            "사용언어": ", ".join(languages) if languages else "선택 안 함",
            "자유의견": comment
        }
        st.session_state.all_responses.append(new_response)
        st.success("🎉 설문조사 제출이 완료되었습니다! 감사합니다.")

# --- 관리자 확인 기능 (사이드바, 기본적으로 접혀있음) ---
with st.sidebar.expander("👨‍💼 관리자 모드", expanded=False):
    password = st.text_input("비밀번호를 입력하세요:", type="password", key="password_input")

    if password == "0501":
        st.success("인증되었습니다.")
        
        st.header("📊 전체 제출 데이터 관리")

        if st.session_state.all_responses:
            all_df = pd.DataFrame(st.session_state.all_responses)

            # --- AI 요약 기능 버튼 ---
            if st.button("🤖 AI로 데이터 요약하기"):
                with st.spinner("AI가 데이터를 분석하고 있습니다... 잠시만 기다려주세요."):
                    summary = get_ai_summary(all_df)
                    st.markdown("### 💡 AI 분석 요약")
                    st.info(summary)

            # --- 데이터 삭제 기능 ---
            indices_to_delete = []
            for i, response in enumerate(st.session_state.all_responses):
                st.subheader(f"응답 {i+1} (제출자: {response['이름']})")
                st.table(pd.DataFrame(response.items(), columns=["항목", "응답"]))
                if st.button(f"응답 {i+1} 삭제하기", key=f"delete_{i}"):
                    indices_to_delete.append(i)

            if indices_to_delete:
                for i in sorted(indices_to_delete, reverse=True):
                    st.session_state.all_responses.pop(i)
                st.rerun()

            st.write("---")
            if st.session_state.all_responses:
                # 삭제가 반영된 후의 데이터를 기준으로 CSV 생성
                updated_df = pd.DataFrame(st.session_state.all_responses)
                csv = updated_df.to_csv(index=False).encode('utf-8-sig')
                st.download_button("남은 데이터 전체 CSV로 다운로드", csv, "survey_responses.csv", "text/csv")
        else:
            st.warning("아직 제출된 데이터가 없습니다.")

    elif password:
        st.error("비밀번호가 틀렸습니다.")