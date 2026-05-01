import requests
from bs4 import BeautifulSoup
import os

DISCORD_WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK')

def get_weather_and_news():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    # --- 1. 날씨 정보 가져오기 ---
    weather_info = "🌡️ 날씨 정보를 가져오지 못했습니다."
    advice = "오늘도 화이팅하세요!"
    try:
        w_url = "https://search.naver.com/search.naver?query=구미+날씨"
        w_res = requests.get(w_url, headers=headers)
        w_soup = BeautifulSoup(w_res.text, 'html.parser')
        
        temp_el = w_soup.find('div', class_='temperature_text')
        status_el = w_soup.find('p', class_='summary')
        
        if temp_el and status_el:
            temp = temp_el.text.replace('현재 온도', '').strip()
            status = status_el.text.split(' ')[-1]
            curr_temp = float(temp.replace('°', ''))
            
            # 온도별 옷차림 조언
            if curr_temp >= 23: advice = "반팔과 얇은 셔츠가 좋겠어요! ☀️"
            elif 17 <= curr_temp < 23: advice = "가디건이나 긴팔을 챙기세요! 🧥"
            elif 12 <= curr_temp < 17: advice = "자켓이나 야상을 입으세요! 🧣"
            else: advice = "많이 추우니 두꺼운 외투를 입으세요! ❄️"
            
            weather_info = f"🌡️ **현재 구미:** {temp} ({status})"
    except: pass

    # --- 2. 뉴스 이슈 3가지 가져오기 ---
    news_info = "📰 뉴스를 가져오지 못했습니다."
    try:
        n_url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=102"
        n_res = requests.get(n_url, headers=headers)
        n_soup = BeautifulSoup(n_res.text, 'html.parser')
        news_list = n_soup.select('.sh_text_headline')[:3]
        if news_list:
            news_info = "\n".join([f"{i+1}. {n.text.strip()}" for i, n in enumerate(news_list)])
    except: pass

    return f"⏰ **아침 7시 브리핑**\n\n{weather_info}\n👕 **추천:** {advice}\n\n📰 **오늘의 이슈 3가지**\n{news_info}"

def main():
    content = get_weather_and_news()
    if DISCORD_WEBHOOK_URL:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": content})
    else:
        print("Webhook URL이 없습니다. Settings를 확인하세요.")

if __name__ == "__main__":
    main()
