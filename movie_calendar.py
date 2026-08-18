import os
import requests
from ics import Calendar, Event
import datetime
import calendar

API_KEY = os.environ.get("TMDB_API_KEY")
LANGUAGE = "ko-KR"
REGION = "KR"

def get_current_month_movies():
    if not API_KEY:
        print("API 키를 찾을 수 없습니다.")
        return []
        
    today = datetime.date.today()
    first_day = today.replace(day=1)
    last_day_of_month = calendar.monthrange(today.year, today.month)[1]
    last_day = today.replace(day=last_day_of_month)
    
    start_date = first_day.strftime("%Y-%m-%d")
    end_date = last_day.strftime("%Y-%m-%d")
    
    print(f"검색 기간: {start_date} ~ {end_date}")
    
    all_movies = []
    page = 1
    
    while True:
        # with_release_type=2|3 (2: 제한 상영, 3: 극장 개봉)
        url = (
            f"https://api.themoviedb.org/3/discover/movie?"
            f"api_key={API_KEY}&language={LANGUAGE}&region={REGION}&"
            f"release_date.gte={start_date}&release_date.lte={end_date}&"
            f"with_release_type=2|3&sort_by=release_date.asc&page={page}"
        )
        
        response = requests.get(url)
        if response.status_code != 200:
            print(f"데이터 조회 실패 (페이지 {page}): {response.status_code}")
            break
            
        data = response.json()
        results = data.get('results', [])
        all_movies.extend(results)
        
        total_pages = data.get('total_pages', 1)
        if page >= total_pages:
            break
            
        page += 1

    print(f"총 {len(all_movies)}편의 개봉작을 수집했습니다.")
    return all_movies

def create_movie_calendar(movies):
    c = Calendar()
    
    for movie in movies:
        title = movie.get('title')
        release_date = movie.get('release_date')
        overview = movie.get('overview', '줄거리 정보가 제공되지 않습니다.')
        
        if not release_date:
            continue
            
        e = Event()
        e.name = f"{title}"
        e.begin = release_date
        e.make_all_day()
        e.description = overview
        
        c.events.add(e)
        
    with open('upcoming_movies.ics', 'w', encoding='utf-8') as f:
        f.writelines(c.serialize_iter())
        
    print("성공적으로 upcoming_movies.ics 파일이 갱신되었습니다!")

if __name__ == "__main__":
    movies = get_current_month_movies()
    if movies:
        create_movie_calendar(movies)
    else:
        print("이번 달 개봉작 정보가 없습니다.")
