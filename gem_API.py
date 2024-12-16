import google.generativeai as genai
import PyPDF2
import os
from typing import List, Dict

class AIChat:
    def __init__(self, api_key: str):
        # API 키 설정 및 모델 초기화
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.chat = None
        self.pdf_content = ""

    def read_pdf(self, pdf_file) -> str:
        """PDF 파일을 읽어서 텍스트로 변환"""
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            self.pdf_content = text
            return "PDF 파일이 성공적으로 로드되었습니다."
        except Exception as e:
            return f"PDF 파일 읽기 실패: {str(e)}"

    def start_chat(self) -> str:
        """새로운 채팅 세션 시작"""
        try:
            context = f"""
            다음은 PDF 문서의 내용입니다. 이 내용을 기반으로 질문에 답변해주세요:
            {self.pdf_content}
            """
            self.chat = self.model.start_chat(history=[])
            self.chat.send_message(context)
            return "채팅이 시작되었습니다. 질문해주세요."
        except Exception as e:
            return f"채팅 시작 실패: {str(e)}"

    def send_message(self, message: str) -> str:
        """사용자 메시지 전송 및 응답 받기"""
        try:
            if not self.chat:
                return "채팅이 시작되지 않았습니다. start_chat()을 먼저 실행해주세요."
            
            response = self.chat.send_message(message)
            return response.text
        except Exception as e:
            return f"메시지 전송 실패: {str(e)}"

    def reset_chat(self) -> str:
        """채팅 세션 초기화"""
        self.chat = None
        self.pdf_content = ""
        return "채팅이 초기화되었습니다."

    def get_chat_history(self) -> List[Dict]:
        """채팅 히스토리 반환"""
        if not self.chat:
            return []
        return self.chat.history
