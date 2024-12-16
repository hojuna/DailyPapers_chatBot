import requests

# URL 설정
arxiv_pdf_url = "https://arxiv.org/pdf/2412.09624"

# 저장할 파일 이름 설정
output_file = "2412.09624.pdf"

# 요청하여 PDF 다운로드
response = requests.get(arxiv_pdf_url)

# HTTP 상태 코드 확인
if response.status_code == 200:
    # PDF 파일 저장
    with open(output_file, "wb") as file:
        file.write(response.content)
    print(f"PDF 파일이 성공적으로 저장되었습니다: {output_file}")
else:
    print(f"PDF 다운로드 실패: {response.status_code}")
