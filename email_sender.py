import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, body, to_email):
    try:
        # 이메일 계정 정보 설정
        from_email = "your_email@example.com"
        password = os.getenv("EMAIL_PASSWORD")
        
        # 이메일 메시지 구성
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        # SMTP 서버 연결 및 이메일 전송
        server = smtplib.SMTP('smtp.example.com', 587)
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print("이메일 전송 성공")
    except Exception as e:
        print(f"이메일 전송 실패: {e}")
