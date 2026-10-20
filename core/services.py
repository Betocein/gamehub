"""Consumo de la API externa RAWG (https://rawg.io/apidocs). La clave se lee del .env."""
import requests
from django.conf import settings
from django.core.cache import cache

API_URL = 'https://api.rawg.io/api/games'


class ApiError(Exception):
    pass


def search_games(query='', page_size=12):
    if not settings.RAWG_API_KEY:
        raise ApiError('Falta la clave RAWG_API_KEY en el archivo .env.')
    cache_key = f'games:{query.lower()}'
    games = cache.get(cache_key)
    if games is None:
        params = {'key': settings.RAWG_API_KEY, 'page_size': page_size}
        if query:
            params['search'] = query
        else:
            params['ordering'] = '-added'
        try:
            resp = requests.get(API_URL, params=params, timeout=8)
            resp.raise_for_status()
            results = resp.json().get('results', [])
        except requests.RequestException:
            raise ApiError('No se pudo obtener la información de la API. Revisa tu clave o tu conexión.')
        games = [{
            'name': g.get('name'),
            'image': g.get('background_image'),
            'released': g.get('released') or 'Sin fecha',
            'rating': g.get('rating'),
            'genres': ', '.join(x['name'] for x in g.get('genres', [])),
        } for g in results]
        cache.set(cache_key, games, 600)  # 10 min, para no gastar peticiones
    return games
