import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import APIError

# 1. 페이지 설정 및 배경 디자인
st.set_page_config(
    page_title="하트가드: 나를 사랑하는 연애 관리",
    page_icon="💖",
    layout="centered"
)

# 고급스러운 배경 및 UI 꾸미기 (CSS)
st.markdown("""
    <style>
    /* 전체 배경에 은은한 핑크-라벤더 그라데이션 */
    .stApp {
        background: linear-gradient(135deg, #FFF5F7 0%, #F0F4FF 100%);
    }
    
    /* 제목 스타일링 */
    .main-title {
        color: #D90429;
        font-size: 3rem !important;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.05);
    }
    
    .sub-title {
        color: #555;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }

    /* 글래스모피즘 스타일 카드 */
    .content-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
        margin-bottom: 20px;
        color: #2B2D42;
    }

    /* 팁 박스 스타일 */
    .tip-box {
        background-color: #FFF0F3;
        border-left: 5px solid #FF4D6D;
        padding: 15px;
        border-radius: 10px;
        font-style: italic;
        margin-bottom: 20px;
    }

    /* 버튼 스타일 커스텀 */
    .stButton>button {
        background: linear-gradient(90deg, #FF4D6D 0%, #FF758F 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(255, 77, 109, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# 2. Gemini API 초기화
if "GEMINI_API_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Secrets에서 'GEMINI_API_KEY'를 설정해주세요.")
    st.stop()

# 3. 헤더 섹션
st.markdown("<h1 class='main-title'>💖 Heart Guard</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>건강한 연애의 시작은 '나'를 돌보는 것부터입니다.</p>", unsafe_allow_html=True)

# 4. [New] 오늘의 연애 자존감 Tip
st.markdown("""
<div class='tip-box'>
    <strong>💌 오늘의 마음 챙김:</strong><br>
    "상대방의 기분을 살피느라 당신의 기분을 놓치지 마세요. 당신이 행복해야 당신의 사랑도 반짝입니다."
</div>
""", unsafe_allow_html=True)

# 5. 탭 구성 (고민 해결 / 나를 위한 심리 / AI 코칭)
tab1, tab2, tab3 = st.tabs(["🔥 상황별 긴급처방", "🌱 나를 위한 심리공부", "🤖 AI 연애 상담소"])

with tab1:
    st.subheader("상황별 마인드셋 솔루션")
    col1, col2 = st.columns(2)
    
    situations = {
        "📱 연락에 집착하게 될 때": "핸드폰을 거실에 두고 샤워를 하거나 책을 딱 10페이지만 읽어보세요. '기다림'을 '나를 위한 시간'으로 재정의하는 연습이 필요해요.",
        "🤬 서운함이 욱하고 올라올 때": "지금 바로 말하지 마세요! 메모장에 서운한 점을 쭉 적어보고 1시간 뒤에 다시 읽어보세요. 감정이 빠진 '팩트'만 전달해야 관계가 건강해집니다.",
        "🥺 상대가 변한 것 같아 불안할 때": "익숙함은 사랑의 식음이 아니라 '안정기'의 증거일 수 있어요. 불안을 해소해달라고 조르기보다, 오늘 하루 내가 즐거웠던 일을 공유하며 긍정적인 에너지를 먼저 보내보세요.",
        "💔 이별 후 자책이 심할 때": "그 연애가 끝난 건 당신이 부족해서가 아니라, 두 사람의 '합'이 거기까지였기 때문이에요. 당신은 그저 그 경험을 통해 한 뼘 더 자란 것뿐입니다."
    }

    keys = list(situations.keys())
    with col1:
        if st.button(keys[0]): st.info(situations[keys[0]])
        if st.button(keys[1]): st.info(situations[keys[1]])
    with col2:
        if st.button(keys[2]): st.info(situations[keys[2]])
        if st.button(keys[3]): st.info(situations[keys[3]])

with tab2:
    st.subheader("자신에 대한 고민 (Self-Reflection)")
    st.write("연애가 힘든 건 기술이 부족해서가 아니라, 내 마음이 지쳤기 때문일 수 있어요.")
    
    self_doubts = {
        "❓ 나는 왜 늘 나쁜 사람만 만날까요?": "당신의 자존감이 낮아져 있어 '나를 함부로 대하는 사람'의 행동을 사랑이라고 착각하고 있을지 몰라요. 나를 귀하게 여기는 연습부터 시작해야 해요.",
        "❓ 제 성격이 너무 예민한 걸까요?": "예민함은 상대의 감정을 잘 읽는 '섬세함'이라는 양날의 검이에요. 그 섬세함을 상대가 아닌 '나의 예술적 취미'나 '자기계발'에 먼저 쏟아보세요.",
        "❓ 저는 연애할 자격이 없는 것 같아요.": "완벽한 사람만 연애하는 게 아닙니다. 부족한 모습 그대로를 서로 보듬어주는 게 연애의 본질이에요. 오늘 거울 속 당신에게 '애썼다'고 한마디만 해주세요."
    }
    
    for question, answer in self_doubts.items():
        with st.expander(question):
            st.write(answer)

with tab3:
    st.subheader("🤖 예외 상황 AI 맞춤 코칭")
    st.write("정해진 답이 없는 복잡한 고민, AI 코치에게 털어놓으세요.")
    
    user_query = st.text_area("고민의 디테일한 상황을 적어주세요.", placeholder="예: 썸남이 3일째 읽씹 중인데, 제가 먼저 선톡해도 없어 보이지 않을까요?")
    
    if st.button("AI 처방전 받기"):
        if user_query:
            with st.spinner("AI 코치가 당신의 매력을 지켜줄 답변을 작성 중..."):
                try:
                    prompt = (
                        "당신은 연애 심리 전문가입니다. 사용자의 고민에 대해 다음 원칙으로 답하세요. "
                        "1. 따뜻하게 공감할 것. 2. 사용자의 자존감을 최우선으로 보호할 것. "
                        "3. 심리학적 근거를 바탕으로 행동 지침을 줄 것. 4. 친근한 말투를 사용할 것."
                    )
                    response = client.models.generate_content(
                        model='gemini-2.5-flash-lite',
                        contents=user_query,
                        config=types.GenerateContentConfig(system_instruction=prompt)
                    )
                    st.markdown(f"<div class='content-card'>{response.text}</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error("오류가 발생했습니다. 다시 시도해주세요.")
        else:
            st.warning("상담 내용을 입력해주세요.")

# 6. 푸터
st.markdown("---")
st.markdown("<p style='text-align: center; color: #888;'>당신은 사랑받기에 충분히 소중한 사람입니다. 오늘도 나를 먼저 사랑하세요. ❤️</p>", unsafe_allow_html=True)
