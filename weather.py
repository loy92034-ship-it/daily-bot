import requests
from bs4 import BeautifulSoup
import os

# 디스코드 웹훅 주소 (깃허브 Secrets에서 가져옴)
DISCORD_WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK')

def get_data():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    # 기본 메시지 설정
    weather_text = "🌡️ 날씨 정보를 가져오지 못했습니다."
    news_text = "📰 뉴스를 가져오지 못했습니다."
    
    # --- 1. 날씨 정보 가져오기 ---
    try:
        w_res = requests.get("https://search.naver.com/search.naver?query=구미+날씨", headers=headers)
        w_soup = BeautifulSoup(w_res.text, 'html.parser')
        temp_el = w_soup.find('div', class_='temperature_text')
        if temp_el:
            temp = temp_el.get_text().replace('현재 온도', '').strip()
            weather_text = f"🌡️ **현재 구미:** {temp}"
    except Exception as e:
        print(f"날씨 에러: {e}")

    # --- 2. 뉴스 이슈 3가지 가져오기 ---
    try:
        n_res = requests.get("https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=102", headers=headers)
        n_soup = BeautifulSoup(n_res.text, 'html.parser')
        news_list = n_soup.select('.sh_text_headline')[:3]
        if news_list:
            news_text = "\n".join([f"{i+1}. {n.get_text().strip()}" for i, n in enumerate(news_list)])
    except Exception as e:
        print(f"뉴스 에러: {e}")

    return f"⏰ **아침 7시 브리핑**\n\n{weather_text}\n\n📰 **오늘의 이슈 3가지**\n{news_text}"

def main():
    final_message = get_data()
    if DISCORD_WEBHOOK_URL:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": final_message})
        print("전송 성공!")
    else:
        print("Webhook URL을 찾을 수 없습니다.")

if __name__ == "__main__":
    main()
