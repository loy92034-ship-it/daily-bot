import requests
from bs4 import BeautifulSoup
import os

# 깃허브 설정에서 넣을 비밀번호 이름을 가져옵니다
DISCORD_WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK')

def get_weather():
    url = "https://search.naver.com/search.naver?query=구미+날씨"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    temp = soup.find('div', class_='temperature_text').text.replace('현재 온도', '').strip()
    status = soup.find('p', class_='summary').text.split(' ')[-1]
    return f"🌡️ **구미 온도:** {temp} ({status})"

def get_top_news():
    url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=102"
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    news_list = soup.select('.sh_text_headline')[:3]
    news_results = [f"{i+1}. {news.text.strip()}" for i, news in enumerate(news_list)]
    return "\n".join(news_results)

def main():
    weather_info = get_weather()
    news_info = get_top_news()
    message = f"⏰ **아침 7시 브리핑**\n\n{weather_info}\n\n📰 **오늘의 이슈 3가지**\n{news_info}\n\n오늘도 화이팅하세요! 💪"
    
    if DISCORD_WEBHOOK_URL:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": message})

if __name__ == "__main__":
    main()
