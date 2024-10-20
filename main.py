import crawl
import os
from datetime import datetime

if __name__ == "__main__":
    today_date = datetime.now().strftime("%Y%m%d")
    if not os.path.exists("papers_pdf/dailypapers_"+today_date+".pdf"):
        crawl.PaperCrawler().crawl_papers()
    else:
        print("이미 오늘의 논문이 존재합니다.")

