import streamlit as pd
import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import APIError

# 1. 페이지 기본 설정 및 디자인 (Theme & Layout)
st.set_page_config(
    page_title="마인드케어 - 나만의 자기관리 AI",
    page_icon="🌱",
    layout="centered"
)

# 커스텀 CSS로 앱 스타일링 (따뜻하고 깔끔한 보라/블루 톤)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    h1 { color: #4A4E69; font-weight: 700; }
    h3 { color: #9A8C98; }
    .stButton>button {
        background-color: #4A4E69;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton>button:hover { background-color: #22223B; color: white; }
    .box {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_index=True)

# 2. Gemini API 클라이언트 초기화 (Streamlit Secrets 활용)
# Streamlit Cloud의 고급 설정(Secrets)에 GEMINI_API_KEY를 등록해야 합니다.
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
else:
    st.error("⚠️ Streamlit Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다. 대시보드 설정을 확인해주세요.")
    st.stop()

# 3. 앱 타이틀 및 소개
st.markdown("<h1>🌱 마인드내비 (MindNavi)</h1>", unsafe_allow_html=True)
st.markdown("<h3>오늘 하루, 당신의 마음과 일상을 정돈해드려요.</h3>", unsafe_allow_html=True)
st.write("---")

# 4. 고정 문답 (자주 겪는 문제점 해결 대시보드)
st.subheader("🔍 지금 나를 방해하는 문제는 무엇인가요?")
st.caption("가장 공감되는 버튼을 클릭하면 즉시 솔루션을 확인할 수 있습니다.")

# 문제점과 정해진 답 데이터베이스
problems = {
    "⏰ 스마트폰 중독 / 도파민 중독": {
        "title": "📱 스마트폰 멀리하기 솔루션",
        "answer": "지금 당장 폰을 **'화면이 바닥을 보게'** 물리적으로 먼 곳에 두세요. 그리고 딱 5분만 스쿼트를 하거나 물을 마시고 오세요. 뇌의 전환에는 5분의 환기가 필요합니다!"
    },
    "💤 무기력증 / 아무것도 하기 싫음": {
        "title": "🛋️ 작은 시작 솔루션",
        "answer": "큰 일을 하려고 하지 마세요. **'침대 이불 정리하기'**, **'일어나서 기지개 켜기'** 같은 1분짜리 초소형 미션부터 시작하세요. 성취감이 뇌를 깨웁니다."
    },
    "🤯 할 일이 너무 많아 혼란스러움": {
        "title": "📝 우선순위 다이어트 솔루션",
        "answer": "종이와 펜을 꺼내 오늘 해야 할 일을 딱 3 가지만 적으세요. 나머지는 내일로 미룹니다. 지금은 그 중 **가장 하기 싫고 중요한 1가지**에만 25분간 집중(뽀모도로)하세요."
    },
    "🥺 불안감 / 타인과의 비교로 인한 우울": {
        "title": "🛑 감정 브레이크 솔루션",
        "answer": "인스타그램이나 SNS 앱을 즉시 종료하세요. 타인의 하이라이트와 나의 비하인드 스토리를 비교하면 불행해집니다. 눈을 감고 깊게 숨을 3번 들이쉬고 내쉬세요."
    }
}

# 4개의 버튼을 2x2 배열로 배치
col1, col2 = st.columns(2)
selected_solution = None

with col1:
    if st.button("⏰ 스마트폰 중독"):
        selected_solution = problems["⏰ 스마트폰 중독 / 도파민 중독"]
    if st.button("🤯 할 일이 넘쳐남"):
        selected_solution = problems["🤯 할 일이 너무 많아 혼란스러움"]

with col2:
    if st.button("💤 무기력증 폭발"):
        selected_solution = problems["💤 무기력증 / 아무것도 하기 싫음"]
    if st.button("🥺 불안감과 우울"):
        selected_solution = problems["🥺 불안감 / 타인과의 비교로 인한 우울"]

# 고정 답변 출력
if selected_solution:
    st.markdown(f"""
    <div class="box">
        <h4>{selected_solution['title']}</h4>
        <p style="font-size: 16px; line-height: 1.6;">{selected_solution['answer']}</p>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# 5. 예외 경우를 위한 AI 상담소 (gemini-2.5-flash-lite 적용)
st.subheader("🤖 예외 상황? AI 자기관리 코치에게 묻기")
st.write("위의 선택지에 없는 구체적인 고민이나 상황이 있다면 아래에 자유롭게 적어주세요.")

user_input = st.text_area(
    "고민 상담 창",
    placeholder="예: 내일 중요한 면접인데 긴장돼서 잠이 안 와요. 어떻게 마음을 다스려야 할까요?",
    height=100
)

if st.button("AI 코칭 받기"):
    if not user_input.strip():
        st.warning("내용을 입력한 후 버튼을 눌러주세요.")
    else:
        with st.spinner("AI 코치가 당신의 고민을 분석하고 솔루션을 찾는 중..."):
            try:
                # 안전하고 친절한 자기관리 코치 프롬프트 설정
                system_instruction = (
                    "당신은 따뜻하고 전문적인 대화형 자기관리 및 동기부여 코치입니다. "
                    "사용자의 고민에 대해 깊이 공감해주고, 행동으로 옮길 수 있는 구체적이고 현실적인 솔루션 2~3가지를 "
                    "친근하고 다정한 말투(해요체)로 번호표(1., 2.)를 붙여 명확하게 제시해주세요."
                )
                
                # gemini-2.5-flash-lite 모델 호출
                response = client.models.generate_content(
                    model='gemini-2.5-flash-lite',
                    contents=user_input,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.7,
                    )
                )
                
                # 결과 출력
                st.markdown("### 💌 AI 코치의 따뜻한 처방전")
                st.markdown(f"""
                <div class="box" style="border-left: 5px solid #4A4E69;">
                    {response.text}
                </div>
                """, unsafe_allow_html=True)
                
            except APIError as e:
                st.error(f"Gemini API 오류가 발생했습니다: {e.message}")
            except Exception as e:
                st.error("알 수 없는 오류가 발생했습니다. 잠시 후 다시 시도해주세요.")

# 6. 하단 푸터 (감성 문구)
st.write("---")
st.caption("💡 오늘 조금 부족했더라도 괜찮아요. 당신은 이미 충분히 잘해내고 있습니다. - 마인드내비")
