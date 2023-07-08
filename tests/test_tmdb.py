from main import tmdb_client
from unittest.mock import Mock
from tmdb_client import api_token
import requests
from main import app

def test_get_poster_url_uses_default_size():
   # Przygotowanie danych
   poster_api_path = "some-poster-path"
   expected_default_size = 'w342'
   # Wywołanie kodu, który testujemy
   poster_url = tmdb_client.get_poster_url(poster_api_path=poster_api_path)
   # Porównanie wyników
   assert expected_default_size in poster_url

def test_get_movies_list_type_popular():
  movies_list = tmdb_client.get_movies_list(list_type="popular")
  assert movies_list is not None

def test_get_movies_list(monkeypatch):
   # Lista, którą będzie zwracać przysłonięte "zapytanie do API"
   mock_movies_list = ['Movie 1', 'Movie 2']

   requests_mock = Mock()
   # Wynik wywołania zapytania do API
   response = requests_mock.return_value
   # Przysłaniamy wynik wywołania metody .json()
   response.json.return_value = mock_movies_list
   monkeypatch.setattr("tmdb_client.requests.get", requests_mock)


   movies_list = tmdb_client.get_movies_list(list_type="popular")
   assert movies_list == mock_movies_list

def test_get_single_movie(monkeypatch):
    mock_movie_id = ['Movie Id']
    requests_mock = Mock()
    response = requests_mock.return_value
    response.json.return_value = mock_movie_id
    monkeypatch.setattr("tmdb_client.requests.get", requests_mock)

    single_movie = tmdb_client.get_single_movie(movie_id="4234234")
    assert single_movie == mock_movie_id


def test_get_single_movie_cast(monkeypatch):
    mock_cast_list = ['Actor 1', 'Actor 2']
    mock_response = Mock()
    mock_response.json.return_value = {'cast': mock_cast_list}
    mock_get = Mock(return_value=mock_response)
    monkeypatch.setattr(requests, 'get', mock_get)

    tmdb_client.api_token = api_token

    single_movie_cast = tmdb_client.get_single_movie_cast(movie_id="4234234")
    assert single_movie_cast == mock_cast_list

def call_tmdb_api(endpoint):
   full_url = f"https://api.themoviedb.org/3/{endpoint}"
   headers = {
       "Authorization": f"Bearer {api_token}"
   }
   response = requests.get(full_url, headers=headers)
   response.raise_for_status()
   return response.json()

def test_homepage(monkeypatch):
   api_mock = Mock(return_value={'results': []})
   monkeypatch.setattr("tmdb_client.call_tmdb_api", api_mock)

   with app.test_client() as client:
       response = client.get('/')
       assert response.status_code == 200
       api_mock.assert_called_once_with('movie/popular')