import requests
from bs4 import BeautifulSoup

def crawl_papers():
    url = "https://huggingface.co/papers"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # 논문 URL 추출 (예시: 페이지의 특정 태그에서 논문 링크 찾기)
        paper_links = soup.find_all('a', class_='paper-link')
        pdf_urls = [link['href'] for link in paper_links if link['href'].endswith('.pdf')]
        
        # PDF 파일 다운로드 및 저장
        for idx, pdf_url in enumerate(pdf_urls):
            pdf_response = requests.get(pdf_url)
            if pdf_response.status_code == 200:
                with open(f"paper_{idx}.pdf", 'wb') as f:
                    f.write(pdf_response.content)
    else:
        print("허깅페이스 페이지 크롤링에 실패했습니다.")
