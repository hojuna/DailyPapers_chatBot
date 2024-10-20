from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 나눔고딕 폰트 등록
pdfmetrics.registerFont(TTFont('NanumGothic', 'NanumGothic.ttf'))

def create_pdf(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    text_object = c.beginText(40, height - 40)
    text_object.setFont("NanumGothic", 12)  # 나눔고딕 폰트 설정

    # 테스트할 한글 텍스트
    text_object.textLine("안녕하세요, 이것은 나눔고딕 폰트를 사용한 테스트입니다.")
    text_object.textLine("이 텍스트가 올바르게 보이면 폰트 설정이 성공한 것입니다.")

    c.drawText(text_object)
    c.save()

# PDF 파일 생성
create_pdf("nanumgothic_test.pdf")