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
        # Selenium 설정 (ChromeDriver 자동 설정)
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(3)  # 묵시적 대기, 활성화를 최대 15초까지 기다린다.

        # 한글 폰트 등록
        pdfmetrics.registerFont(TTFont('NanumGothic', 'NanumGothic.ttf'))

    def sanitize_filename(self, filename):
        # 파일 이름에서 허용되지 않는 문자를 제거
        return re.sub(r'[<>:"/\\|?*]', '', filename)

    def translate_papago(self, text: str):
        # Papago 사이트로 이동
        self.driver.get('https://papago.naver.com/')

        # 텍스트 입력창 찾기
        input_box = self.driver.find_element("css selector", 'textarea#txtSource')  # textarea로 변경
        
        # 입력창에 텍스트 입력
        input_box.clear()  # 기존 텍스트 삭제
        input_box.send_keys(text)

        # 번역이 완료될 때까지 대기
        time.sleep(3)

        # 번역 결과 가져오기
        translated_text = self.driver.find_element("css selector", 'div#txtTarget').text

        if translated_text=="":
            time.sleep(3)
            translated_text = self.driver.find_element("css selector", 'div#txtTarget').text

        return translated_text

    def save_to_pdf(self, filename, data):
        c = canvas.Canvas(filename, pagesize=landscape(letter))  # 가로 방향 설정
        width, height = landscape(letter)

        for item in data:
            text_object = c.beginText(40, height - 40)
            text_object.setFont("NanumGothic", 12)  # 한글 폰트 설정

            text_object.textLine(f"제목: {item['title']}")
            text_object.textLine("")  # 빈 줄 추가
            # 요약 텍스트 줄바꿈
            wrapped_abstract = textwrap.wrap(item['abstract'], width=80)  # 너비에 맞게 줄바꿈
            text_object.textLine("번역된 요약:")
            for line in wrapped_abstract:
                text_object.textLine(line)
            text_object.textLine("")  # 빈 줄 추가
            text_object.textLine(f"URL: {item['url']}")
            text_object.textLine("")  # 빈 줄 추가

            c.drawText(text_object)
            c.showPage()  # 새로운 페이지 시작

        c.save()

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

            for link in paper_links:
                title = link.text.strip()  # 논문 제목 추출
                paper_url = "https://huggingface.co" + link['href']
                # print(f"제목: {title}")
                # print(f"URL: {paper_url}")
                
                # Papago에서 제목 번역
                translated_title = self.translate_papago(title)
                print(f"번역된 제목: {translated_title}")

                response_paper = requests.get(paper_url)
                if response_paper.status_code == 200:
                    soup_paper = BeautifulSoup(response_paper.text, 'html.parser')
                    
                    # 논문 요약 추출 (요약 부분이 있을 경우)
                    paper_abstract = soup_paper.find('p', class_='text-gray-700 dark:text-gray-400')
                    
                    if paper_abstract:
                        abstract_text = paper_abstract.text.strip()
                        # print(f"요약: {abstract_text}")
                        
                        # Papago에서 요약 번역
                        translated_abstract = self.translate_papago(abstract_text)
                        # print(f"번역된 요약: {translated_abstract}")

                        # 데이터를 리스트에 추가
                        papers_data.append({
                            "title": translated_title,
                            "abstract": translated_abstract,
                            "url": paper_url
                        })
                    else:
                        print(f"요약을 찾을 수 없습니다: {paper_url}")
                else:
                    print(f"논문 페이지 접근 실패. 상태 코드: {response_paper.status_code}")
                
                print()  # 각 논문 정보 사이에 빈 줄 추가

            # 오늘 날짜를 가져와서 파일 이름에 추가
            today_date = datetime.now().strftime("%Y%m%d")
            pdf_filename = f"DailyPapers_{today_date}.pdf"
            pdf_path = os.path.join(save_dir, pdf_filename)
            self.save_to_pdf(pdf_path, papers_data)
            print(f"PDF 파일 저장 완료: {pdf_path}")

        else:
            print("허깅페이스 페이지 크롤링에 실패했습니다.")

    def close(self):
        # 작업 완료 후 브라우저 닫기
        self.driver.quit()

# 실행
if __name__ == "__main__":
    crawler = PaperCrawler()
    try:
        crawler.crawl_papers()
    finally:
        crawler.close()
