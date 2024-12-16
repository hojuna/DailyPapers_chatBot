import os
import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import textwrap
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class PaperCrawler:
    def __init__(self):
        pass

    def sanitize_filename(self, filename):
        # 파일 이름에서 허용되지 않는 문자를 제거
        return re.sub(r'[<>:"/\\|?*]', '', filename)
    
    def download_pdf(self, url, title):
        url = url.replace("papers/", "")
        # URL 설정
        arxiv_pdf_url = "https://arxiv.org/pdf" + url

        # 저장할 파일 이름 설정
        output_file = title + ".pdf"

        # 저장 디렉토리 생성
        os.makedirs(os.path.join(os.getcwd(), "papers_pdf"), exist_ok=True)
        save_dir = os.path.join(os.getcwd(), "papers_pdf")
        output_path = os.path.join(save_dir, output_file)

        # 파일이 이미 존재하는지 확인
        if os.path.exists(output_path):
            print(f"파일이 이미 존재합니다: {output_path}")
            return

        # 요청하여 PDF 다운로드
        response = requests.get(arxiv_pdf_url)

        # HTTP 상태 코드 확인
        if response.status_code == 200:
            # PDF 파일 저장
            with open(output_path, "wb") as file:
                file.write(response.content)
            print(f"PDF 파일이 성공적으로 저장되었습니다: {output_path}")
        else:
            print("url: ", arxiv_pdf_url, "title: ", title)
            print(f"PDF 다운로드 실패: {response.status_code}")


    def crawl_papers(self):
        url = "https://huggingface.co/papers"
        save_dir = os.path.join(os.getcwd(), "papers_pdf")
        
        # 저장 디렉토리 생성
        os.makedirs(save_dir, exist_ok=True)

        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            paper_links = soup.find_all('a', class_='line-clamp-3 cursor-pointer text-balance')
            
            papers_data = []  # 데이터를 저장할 리스트

            for link in paper_links[:10]:
                title = link.text.strip()  # 논문 제목 추출
                paper_url = "https://huggingface.co" + link['href']

                self.download_pdf(link['href'], title)
                papers_data.append(title)
        else:
            print("허깅페이스 페이지 크롤링에 실패했습니다.")

        return papers_data


# 실행
if __name__ == "__main__":
    crawler = PaperCrawler()
    try:
        crawler.crawl_papers()
    finally:
        pass