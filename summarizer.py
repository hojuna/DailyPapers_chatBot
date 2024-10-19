import openai
import os

# GPT API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_paper(text):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"다음 논문의 요약을 작성해줘: {text[:2000]}",  # 최대 입력 길이를 고려하여 텍스트 잘라내기
            max_tokens=150
        )
        summary = response.choices[0].text.strip()
        return summary
    except Exception as e:
        print(f"요약 생성 실패: {e}")
        return "요약 생성 실패"
