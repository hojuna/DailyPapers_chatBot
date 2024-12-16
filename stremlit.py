import streamlit as st
import time
from crawl import PaperCrawler
from gem_API import AIChat
import os

# 스트림릿 페이지 기본 설정
st.set_page_config(page_title="챗봇", page_icon="🤖")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_active" not in st.session_state:
    st.session_state.conversation_active = False
if "selected_title" not in st.session_state:
    st.session_state.selected_title = None
if "ai_chat" not in st.session_state:
    # API 키는 환경 변수나 안전한 방법으로 관리해야 합니다
    api_key = os.getenv("GEMINI_API_KEY")
    st.session_state.ai_chat = AIChat(api_key)

@st.cache_resource
def get_paper_data():
    paper_crawler = PaperCrawler()
    crawled_titles = paper_crawler.crawl_papers()
    return crawled_titles

# 제목 표시
st.title("huggingface daily paper chatbot 🤖")

# PDF 파일 업로더 추가
uploaded_file = st.file_uploader("PDF 파일을 업로드하세요", type="pdf")
if uploaded_file is not None:
    result = st.session_state.ai_chat.read_pdf(uploaded_file)
    st.success(result)
    # PDF 로드 후 채팅 시작
    start_result = st.session_state.ai_chat.start_chat()
    st.info(start_result)

crawled_titles = get_paper_data()

# 대화 종료 함수
def end_conversation():
    st.session_state.conversation_active = False
    st.session_state.selected_title = None
    st.session_state.messages = []
    st.session_state.ai_chat.reset_chat()

# 사이드바에 타이틀 버튼 표시
st.sidebar.header("크롤링된 타이틀")

# 타이틀 버튼들
for title in crawled_titles:
    button_disabled = st.session_state.conversation_active and st.session_state.selected_title != title
    if st.sidebar.button(title, disabled=button_disabled):
        st.session_state.messages = []  # 대화 내용 초기화
        st.session_state.conversation_active = True
        st.session_state.selected_title = title
        
        # PDF 파일 경로 생성
        pdf_path = f"/Users/ihojun/project/DailyPapers_in_hug/papers_pdf/{title}.pdf"
        
        # PDF 파일 존재 확인
        if os.path.exists(pdf_path):
            # PDF 파일 읽기
            with open(pdf_path, 'rb') as pdf_file:
                result = st.session_state.ai_chat.read_pdf(pdf_file)
                st.success(f"PDF 파일을 성공적으로 로드했습니다: {title}")
                
                # PDF 로드 후 채팅 시작
                start_result = st.session_state.ai_chat.start_chat()
                st.info(start_result)
        else:
            st.error(f"PDF 파일을 찾을 수 없습니다: {title}")
            st.session_state.conversation_active = False
            
        st.session_state.messages.append({"role": "user", "content": f"선택한 타이틀: {title}"})

# 메인 채팅 영역
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력
if prompt := st.chat_input("메시지를 입력하세요", disabled=not st.session_state.conversation_active):
    # 사용자 메시지 표시
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # AI 응답 처리
    with st.chat_message("assistant"):
        with st.spinner("생각 중..."):
            response = st.session_state.ai_chat.send_message(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# 대화 종료 버튼 (하단에 배치)
col1, col2, col3 = st.columns([1,1,1])
with col2:
    if st.button("대화 종료", disabled=not st.session_state.conversation_active):
        end_conversation()
        st.rerun()

# 현재 대화 상태 표시
if st.session_state.conversation_active:
    st.sidebar.info(f"현재 선택된 주제: {st.session_state.selected_title}")
else:
    st.sidebar.info("새로운 주제를 선택해주세요")
