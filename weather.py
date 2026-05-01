import requests
from bs4 import BeautifulSoup
import os

# 디스코드 주소 가져오기
DISCORD_WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK')

def get_weather():
    # 1. '사람인 척' 하기 위한 헤더 설정 (네이버 차단 방지)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    url = "https://search.naver.com/search.naver?query=구미+날씨"
    
    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 2. 정보가 있는지 먼저 확인하고 가져오기 (에러 방지)
        temp_element = soup.find('div', class_='temperature_text')
        status_element = soup.find('p', class_='summary')
        
        if temp_element and status_element:
            temp = temp_element.text.replace('현재 온도', '').strip()
            status = status_element.text.split(' ')[-1]
            return f"🌡️ **구미 온도:** {temp} ({status})"
        else:
            return "🌡️ 날씨 정보를 찾을 수 없습니다. (페이지 구조 변경 가능성)"
            
    except Exception as e:
        return f"🌡️ 날씨 수집 중 오류 발생: {e}"

def get_top_news():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=102"
    
    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 뉴스 제목 추출
        news_list = soup.select('.sh_text_headline')[:3]
        if not news_list:
            return "📰 현재 주요 뉴스를 가져올 수 없습니다."
            
        results = []
        for i, news in enumerate(news_list):
            results.append(f"{i+1}. {news.text.strip()}")
        return "\n".join(results)
        
    except Exception as e:
        return f"📰 뉴스 수집 중 오류 발생: {e}"

def main():
    weather_info = get_weather()
    news_info = get_top_news()
    
    message = (
        f"⏰ **아침 7시 브리핑**\n\n"
        f"{weather_info}\n\n"
        f"📰 **오늘의 이슈 3가지**\n"
        f"{news_info}\n\n"
        f"오늘도 좋은 하루 보내세요! 💪"
    )
    
    if DISCORD_WEBHOOK_URL:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
        print("디스코드로 전송을 완료했습니다!")
    else:
        print("Webhook URL이 설정되지 않았습니다. Secrets 설정을 확인해주세요.")

if __name__ == "__main__":
    main()
