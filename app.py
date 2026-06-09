import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import APIError

# 1. 페이지 설정 및 배경 디자인
st.set_page_config(
    page_title="마인드내비 - 일상 & 연애 자기관리",
    page_icon="🌱",
    layout="centered"
)

# 감성적이면서도 깔끔한 무드의 커스텀 CSS
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #FFF5F7 0%, #F4F7FF 100%); }
    .main-title { color: #4A4E69; font-size: 2.8rem !important; font-weight: 800; text-align: center; margin-bottom: 5px; }
    .sub-title { color: #666; text-align: center; font-size: 1.1rem; margin-bottom: 25px; }
    .content-card {
        background: rgba(255, 255, 255, 0.85);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(74, 78, 105, 0.15);
        box-shadow: 0 4px 15px rgba(0,0,0,0.04);
        margin-bottom: 15px;
        color: #2B2D42;
    }
    .stButton>button {
        background: linear-gradient(90deg, #4A4E69 0%, #9A8C98 100%);
        color: white; border: none; border-radius: 10px; padding: 10px; font-weight: 600; width: 100%;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 10px rgba(74, 78, 105, 0.3); }
    </style>
""", unsafe_allow_html=True)

# 2. Gemini API 초기화
if "GEMINI_API_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Secrets에서 'GEMINI_API_KEY'를 설정해주세요.")
    st.stop()

# 3. 헤더
st.markdown("<h1 class='main-title'>🌱 마인드내비 (MindNavi)</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>일상의 무기력함부터 연애의 흔들림까지, 나를 지키는 자기관리</p>", unsafe_allow_html=True)

# --- 🌡️ 실시간 마음 흔들림 온도계 ---
st.markdown("<div class='content-card'>", unsafe_allow_html=True)
st.markdown("#### 🌡️ 지금 나의 멘탈 흔들림 지수")
anxiety_score = st.slider("현재 내 마음의 불안도나 스트레스는 어느 정도인가요?", 0, 100, 30)
if anxiety_score >= 70:
    st.error(f"🚨 **위험 (불안도 {anxiety_score}%)**: 감정 에너지가 과부하된 상태입니다. 즉시 하던 일을 멈추고 심호흡을 하세요.")
elif anxiety_score >= 40:
    st.warning(f"💛 **주의 (불안도 {anxiety_score}%)**: 서운함, 잡념, 혹은 무기력이 시작되고 있네요. 환기가 필요한 시점입니다.")
else:
    st.success(f"💚 **안정 (불안도 {anxiety_score}%)**: 일상과 감정의 밸런스가 아주 좋습니다. 이 상태를 유지해보세요!")
st.markdown("</div>", unsafe_allow_html=True)


# 4. 기능별 대시보드 탭 구성
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔥 일상 해결", "💘 연애 해결", "🌱 자존감 진단", "💬 카톡 속마음", "🤖 AI 상담소"])

# 탭 1: 일상 자기관리 고정 문답 (원래 기능 반영)
with tab1:
    st.markdown("### 🔍 내 일상을 방해하는 문제점 해결")
    st.caption("가장 공감되는 나만의 일상 문제를 선택해 즉시 솔루션을 확인하세요.")
    
    col1, col2 = st.columns(2)
    daily_problems = {
        "⏰ 스마트폰 중독 / 도파민 중독": "지금 당장 폰을 **'화면이 바닥을 보게'** 물리적으로 먼 곳에 두세요. 그리고 딱 5분만 스쿼트를 하거나 물을 마시고 오세요. 뇌의 회로를 바꾸는 데는 5분의 환기가 필요합니다.",
        "💤 무기력증 / 아무것도 하기 싫음": "큰 일을 하려고 하지 마세요. **'침대 이불 정리하기'**, **'일어나서 기지개 켜기'** 같은 1분짜리 초소형 미션부터 시작하세요. 아주 작은 성취감이 뇌를 깨웁니다.",
        "🤯 할 일이 너무 많아 혼란스러움": "종이와 펜을 꺼내 오늘 해야 할 일을 딱 3 가지만 적으세요. 나머지는 내일로 미룹니다. 지금은 그 중 **가장 하기 싫고 중요한 1가지**에만 25분간 집중하세요.",
        "🥺 타인과의 비교로 인한 우울": "인스타그램이나 SNS 앱을 즉시 종료하세요. 타인의 하이라이트와 나의 비하인드 스토리를 비교하면 불행해집니다. 시선을 내 방, 내 일상으로 돌리세요."
    }
    keys_daily = list(daily_problems.keys())
    with col1:
        if st.button("⏰ 스마트폰 중독"): st.info(daily_problems[keys_daily[0]])
        if st.button("🤯 할 일이 넘쳐남"): st.info(daily_problems[keys_daily[2]])
    with col2:
        if st.button("💤 무기력증 폭발"): st.info(daily_problems[keys_daily[1]])
        if st.button("🥺 비교와 우울감"): st.info(daily_problems[keys_daily[3]])

# 탭 2: 연애 멘탈케어 고정 문답
with tab2:
    st.markdown("### 🚨 내 연애를 흔드는 순간, 행동 지침")
    st.caption("상대방에게 휘둘리지 않고 내 중심을 잡기 위한 멘탈 처방전입니다.")
    
    col3, col4 = st.columns(2)
    love_problems = {
        "📱 연락에 과도하게 집착하게 될 때": "상대방의 답장에 내 행복을 저당 잡히지 마세요. 지금 알림을 무음으로 끄고, 내가 좋아하는 영상을 보거나 밖으로 산책을 나가세요. 내가 바쁠 때 연애 주도권도 따라옵니다.",
        "🤬 서운함이 욱하고 올라올 때": "메모장에 서운한 이유를 감정 빼고 글로 적어보세요. 1시간 뒤에 다시 읽어보면 홧김에 해서 상처 줄 말들을 걸러내고 건강한 대화를 할 수 있습니다.",
        "🎣 어장관리 당하는 것 같을 때": "나를 헷갈리게 하는 사람은 나를 좋아하지 않는 겁니다. 과감하게 한 걸음 물러서서 내 일상에 집중해 보세요. 굳이 애매한 인연에 에너지를 쓸 필요 없습니다.",
        "💔 이별 후 전연인 SNS 염탐할 때": "전연인의 SNS는 내 멘탈을 갉아먹는 독입니다. 지금 즉시 차단하거나 숨김 처리하세요. 과거의 미련을 냉정하게 잘라내야 더 가치 있는 다음 사랑이 찾아옵니다."
    }
    keys_love = list(love_problems.keys())
    with col3:
        if st.button("📱 연락에 자꾸 집착해요"): st.info(love_problems[keys_love[0]])
        if st.button("🎣 어장관리 인가요?"): st.info(love_problems[keys_love[2]])
    with col4:
        if st.button("🤬 사소한 일에 서운해요"): st.info(love_problems[keys_love[1]])
        if st.button("💔 이별 후 미련이 남아요"): st.info(love_problems[keys_love[3]])

# 탭 3: 내 연애 자존감 체크리스트 (자신에 대한 고민)
with tab3:
    st.markdown("### 🌱 내 연애 자존감 및 매력 진단")
    st.write("대부분의 연애 고민은 '나를 얼마나 소중히 여기는가'에서 출발합니다. 스스로 체크해 보세요.")
    
    q1 = st.checkbox("상대방의 기분이나 반응에 내 하루 전체가 롤러코스터를 탄다.")
    q2 = st.checkbox("서운한 게 있어도 상대가 싫어하거나 떠나갈까 봐 솔직하게 말하지 못한다.")
    q3 = st.checkbox("나 자신에게 투자하는 시간(취미, 공부)보다 상대를 기다리는 시간이 훨씬 길다.")
    q4 = st.checkbox("가끔 '내가 매력이 없어서 상대가 이러나?' 하는 자책감이 든다.")
    
    score = sum([q1, q2, q3, q4])
    if score >= 3:
        st.markdown("<div style='color:#D90429; font-weight:bold;'>⚠️ 경고: 연애 올인 및 자아 상실 단계</div><p>상대방 중심의 연애를 하고 있어 자존감이 많이 낮아진 상태입니다. 오늘부터 연락을 조금 줄이고 오롯이 나만을 위한 저녁 시간을 보내세요.</p>", unsafe_allow_html=True)
    elif score >= 1:
        st.markdown("<div style='color:#CC5A01; font-weight:bold;'>💛 주의: 감정 휘둘림 시작 단계</div><p>중심이 살짝 흔들리고 있습니다. 상대방은 내 삶의 전부가 아닌 '일부'라는 점을 명심하고, 내 일상의 루틴을 다시 세워보세요.</p>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='color:#2B9348; font-weight:bold;'>💚 안전: 단단한 내면의 독립형 연애</div><p>자존감이 높고 건강한 상태입니다. 상대방과 균형 잡힌 사랑을 하고 계시네요. 지금처럼 나를 아끼며 연애를 즐기세요!</p>", unsafe_allow_html=True)

# 탭 4: 카톡 말투 속마음 통역기
with tab4:
    st.markdown("### 💬 카톡 말투로 읽는 유머러스 속마음 가이드")
    st.write("상대의 애매한 카톡 스타일 때문에 전전긍긍하고 있다면? 가볍게 확인해 보세요.")
    
    talk_style = st.selectbox(
        "상대방의 가장 특징적인 카톡 스타일은?",
        ["스타일을 선택하세요", "갑자기 짧아진 단답형 (ㅇㅇ, 웅, 그래)", "사소한 일상도 다 물어보는 질문형", "읽고 한참 뒤에 오는 굼벵이형", "이모티콘과 리액션이 폭발하는 과즙형"]
    )
    
    if talk_style == "갑자기 짧아진 단답형 (ㅇㅇ, 웅, 그래)":
        st.error("💡 통역: 현재 다른 일로 매우 바쁘거나 심리적 에너지가 고갈된 상태입니다. 이때 '왜 단답해?'라고 따지면 싸움만 납니다. 똑같이 쿨하게 대하고 내 할 일 하러 가세요.")
    elif talk_style == "사소한 일상도 다 물어보는 질문형":
        st.success("💡 통역: 대화를 계속 이어가고 싶어 안달이 난 상태, 즉 그린라이트 확률 95%! 상대방도 당신의 반응을 기다리고 있으니 다정하게 응답해 주셔도 좋습니다.")
    elif talk_style == "읽고 한참 뒤에 오는 굼벵이형":
        st.warning("💡 통역: 연락에 원래 무디거나, 현재 당신보다 더 재밌는 우선순위(게임, 친구, 일)가 있는 상태입니다. 선톡을 뚝 끊고 상대가 먼저 나를 찾을 때까지 밀당 게이지를 올리세요.")
    elif talk_style == "이모티콘과 리액션이 폭발하는 과즙형":
        st.success("💡 통역: 당신에게 아주 잘 보이고 싶어 정성을 들이는 중입니다. 리액션에 대한 칭찬이나 고마움을 살짝 표현해 주면 관계가 더 돈독해집니다.")

# 탭 5: 예외 상황 맞춤형 AI 코칭 (gemini-2.5-flash-lite)
with tab5:
    st.markdown("### 🤖 무엇이든 물어보는 AI 자기관리 코치")
    st.write("일상의 무기력, 일 관리 슬럼프부터 아무에게도 말 못 할 미묘한 연애 고민까지 디테일하게 적어주세요.")
    
    user_query = st.text_area("나의 구체적인 상황과 고민", placeholder="예시 1: 시험 기간인데 자꾸 폰만 보게 돼요.\n예시 2: 썸남이 며칠째 읽씹 중인데 먼저 연락하면 없어 보일까요?")
    
    if st.button("AI 맞춤 처방전 받기"):
        if user_query.strip():
            with st.spinner("AI 코치가 당신의 삶의 균형과 자존감을 지켜줄 정답을 분석 중..."):
                try:
                    # 일상과 연애 자존감을 포괄하는 전문적인 멘토 페르소나
                    prompt = (
                        "당신은 일상 자기관리 및 연애 심리 전문가이자, 사용자의 자존감 수호를 최우선으로 여기는 멘토입니다. "
                        "사용자의 고민(일상 슬럼프 또는 연애 고민 등)을 분석하여 다음 원칙에 맞춰 대답하세요. "
                        "1. 따뜻하게 공감할 것. "
                        "2. 일상의 루틴을 회복하고 내면을 단단하게 지킬 수 있는 현실적이고 구체적인 행동 가이드를 2~3가지(번호 매기기)로 제시할 것. "
                        "3. 타인이나 상황에 휘둘리지 말고 자신을 가장 먼저 사랑하라는 메시지로 마무리할 것. 말투는 친근하면서도 뼈가 있는 해요체를 쓰세요."
                    )
                    response = client.models.generate_content(
                        model='gemini-2.5-flash-lite',
                        contents=user_query,
                        config=types.GenerateContentConfig(system_instruction=prompt)
                    )
                    st.markdown(f"<div class='content-card' style='border-left:5px solid #4A4E69; background-color:#FFFDFD;'>{response.text}</div>", unsafe_allow_html=True)
                except APIError as e:
                    st.error(f"Gemini API 오류가 발생했습니다: {e.message}")
                except Exception as e:
                    st.error("오류가 발생했습니다. 잠시 후 다시 시도해 주세요.")
        else:
            st.warning("상담받을 고민 내용을 입력해 주세요.")

# 5. 푸터
st.markdown("---")
st.markdown("<p style='text-align: center; color: #888;'>당신의 일상도, 당신의 사랑도 결국 '나 자신'이 바로 서야 행복해집니다. 오늘도 화이팅! 🌿❤️</p>", unsafe_allow_html=True)
