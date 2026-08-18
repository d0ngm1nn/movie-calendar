import os
import requests
from ics import Calendar, Event

# GitHub Secrets에서 API 키를 불러옵니다.
API_KEY = os.environ.get("TMDB_API_KEY")
LANGUAGE = "ko-KR"
REGION = "KR"

def get_upcoming_movies():
    if not API_KEY:
        print("API 키를 찾을 수 없습니다.")
        return []
        
    url = f"https://api.themoviedb.org/3/movie/upcoming?api_key={API_KEY}&language={LANGUAGE}&region={REGION}&page=1"
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
        
    print("성공적으로 upcoming_movies.ics 파일이 갱신되었습니다!")

if __name__ == "__main__":
    movies = get_upcoming_movies()
    if movies:
        create_movie_calendar(movies)
