import os
import requests
from ics import Calendar, Event
import datetime
import calendar

# GitHub Secrets에서 API 키를 불러옵니다.
API_KEY = os.environ.get("TMDB_API_KEY")
LANGUAGE = "ko-KR"
REGION = "KR"

def get_current_month_movies():
    if not API_KEY:
        print("API 키를 찾을 수 없습니다.")
        return []
        
    # 1. 이번 달의 시작일과 마지막 일자 계산
    today = datetime.date.today()
    first_day = today.replace(day=1)
    last_day_of_month = calendar.monthrange(today.year, today.month)[1]
    last_day = today.replace(day=last_day_of_month)
    
    start_date = first_day.strftime("%Y-%m-%d")
    end_date = last_day.strftime("%Y-%m-%d")
    
    print(f"검색 기간: {start_date} ~ {end_date}")
    
    # 2. TMDB Discover API를 사용하여 정확한 날짜 범위로 검색 (개봉일 오름차순 정렬)
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&language={LANGUAGE}&region={REGION}&primary_release_date.gte={start_date}&primary_release_date.lte={end_date}&sort_by=primary_release_date.asc"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        print(f"데이터를 가져오는데 실패했습니다. 상태 코드: {response.status_code}")
        return []

def create_movie_calendar(movies):
    c = Calendar()
    
    for movie in movies:
        title = movie.get('title')
        release_date = movie.get('release_date')
        overview = movie.get('overview', '줄거리 정보가 제공되지 않습니다.')
        
        if not release_date:
            continue
            
        e = Event()
        e.name = f"🎬 개봉: {title}"
        e.begin = release_date
        e.make_all_day()
        e.description = overview
        
        c.events.add(e)
        
    with open('upcoming_movies.ics', 'w', encoding='utf-8') as f:
        f.writelines(c.serialize_iter())
        
    print("성공적으로 이번 달 영화 캘린더 파일(upcoming_movies.ics)이 갱신되었습니다!")

if __name__ == "__main__":
    movies = get_current_month_movies()
    if movies:
        create_movie_calendar(movies)
    else:
        print("이번 달 개봉작 정보가 없습니다.")
