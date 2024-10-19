# workflow.py
import os
from crawl import crawl_papers
from pdf_processor import pdf_to_text
from summarizer import summarize_paper
from email_sender import send_email

# 전체 워크플로우를 실행하는 함수
def run_daily_workflow():
    # 논문 크롤링 및 저장
    crawl_papers()
    
    # 다운로드된 논문 파일 리스트 가져오기
    pdf_files = [f for f in os.listdir() if f.endswith('.pdf')]
    summaries = []
    
    # 각 논문을 요약하고 리스트에 저장
    for pdf_file in pdf_files:
        text = pdf_to_text(pdf_file)
        if text:
            summary = summarize_paper(text)
            summaries.append(f"{pdf_file} 요약: {summary}\n")
    
    # 이메일 내용 구성 및 전송
    email_body = "\n".join(summaries)
    send_email("오늘의 논문 요약", email_body, "recipient@example.com")
